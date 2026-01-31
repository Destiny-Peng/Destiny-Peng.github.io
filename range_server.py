#!/usr/bin/env python3
import http.server
import socketserver
import sys
import os
import re

class RangeRequestHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()
        if not os.path.exists(path):
            self.send_error(404, "File not found")
            return None
        f = open(path, 'rb')
        fs = os.fstat(f.fileno())
        size = fs.st_size
        start = 0
        end = size - 1

        range_header = self.headers.get('Range')
        if range_header:
            m = re.match(r'bytes=(\d+)-(\d*)', range_header)
            if m:
                start = int(m.group(1))
                if m.group(2):
                    end = int(m.group(2))
                self.send_response(206)
                self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
                self.send_header('Accept-Ranges', 'bytes')
                self.send_header('Content-Length', str(end - start + 1))
            else:
                self.send_response(200)
                self.send_header('Content-Length', str(size))
        else:
            self.send_response(200)
            self.send_header('Content-Length', str(size))

        ctype = self.guess_type(path)
        self.send_header('Content-type', ctype)
        self.send_header('Last-Modified', self.date_time_string(fs.st_mtime))
        self.end_headers()
        f.seek(start)
        self.range = (start, end)
        return f

    def copyfile(self, source, outputfile):
        start, end = getattr(self, 'range', (0, None))
        source.seek(start)
        tosend = None if end is None else (end - start + 1)
        bufsize = 64 * 1024
        while tosend is None or tosend > 0:
            read = bufsize if tosend is None or tosend > bufsize else tosend
            data = source.read(read)
            if not data:
                break
            outputfile.write(data)
            if tosend is not None:
                tosend -= len(data)


def run(port=8000):
    with socketserver.TCPServer(("", port), RangeRequestHandler) as httpd:
        print(f"Serving on port {port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run(port)
