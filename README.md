# 个人主页（GitHub Pages）

这是一个简单的静态个人主页模板，已放在项目根目录。修改 `index.html` 中的内容以替换为你的个人信息。

本地预览：

```bash
# 在仓库根目录运行一个简单的静态服务器
python3 -m http.server 8000
# 然后在浏览器打开 http://localhost:8000
```

部署到 GitHub Pages：

1. 将仓库推送到 `gh-pages` 分支或启用 `main`/`master` 的 GitHub Pages（仓库设置中）。
2. 等待几分钟，站点将通过 `https://<你的用户名>.github.io/<仓库名>/` 提供服务，若这是个人主页仓库（以 username.github.io 命名），则在 `https://<你的用户名>.github.io/` 下可访问。

要点：
- 编辑 `index.html` 中的姓名、简介、项目与联系方式。
- 可替换 `assets/css/style.css` 以更改配色和布局。
