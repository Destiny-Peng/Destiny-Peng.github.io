document.addEventListener("DOMContentLoaded", function () {
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
});

// Flowchart <-> video sync
document.addEventListener("DOMContentLoaded", function () {
  var video = document.getElementById("project-video-hero");
  if (!video) return;

  // Find the overlay and its local caption so we update the correct caption
  var overlay = document.querySelector(".flowchart-overlay");
  if (!overlay) return;
  var regions = Array.from(overlay.querySelectorAll(".region"));
  var caption = overlay
    .closest(".flowchart-container")
    .querySelector(".flowchart-caption");

  // Parse time ranges
  var parsed = regions.map(function (el) {
    return {
      el: el,
      start: parseFloat(el.getAttribute("data-start")) || 0,
      end: parseFloat(el.getAttribute("data-end")) || 0,
      title: el.getAttribute("data-title") || "",
    };
  });

  // Update highlights based on current time
  function updateHighlights() {
    var t = video.currentTime;
    var activeShown = false;
    parsed.forEach(function (r) {
      if (t >= r.start && t < r.end) {
        r.el.classList.add("active");
        if (caption && !activeShown) {
          caption.textContent = r.title;
          activeShown = true;
        }
      } else {
        r.el.classList.remove("active");
      }
    });
    if (caption && !activeShown) caption.textContent = "";
  }

  var rafScheduled = false;
  video.addEventListener("timeupdate", function () {
    if (!rafScheduled) {
      rafScheduled = true;
      requestAnimationFrame(function () {
        updateHighlights();
        rafScheduled = false;
      });
    }
  });

  // Clicking a region seeks video to its start time
  parsed.forEach(function (r) {
    r.el.setAttribute("tabindex", "0");
    r.el.addEventListener("click", function () {
      video.currentTime = r.start;
      video.play();
    });
    r.el.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        video.currentTime = r.start;
        video.play();
      }
    });
  });

  // initialize once
  updateHighlights();
});
