# AI Daily Digest

每日AI精选资讯，汇聚全球人工智能领域最新动态。

## 访问网站

🌐 **https://dengbiao.github.io/ai-daily-digest/**

## 特性

- 🤖 每日自动抓取AI领域最新资讯
- 📊 精选5-10条高质量信息
- 🔗 每条信息多源验证，可溯源
- 📱 响应式设计，适配各种设备
- 📅 每日独立详情页
- 🔍 首页新闻列表浏览

## 技术栈

- **生成器**: Python + Jekyll
- **样式**: Tailwind CSS
- **托管**: GitHub Pages
- **自动化**: GitHub Actions + OpenClaw Cron

## 目录结构

```
.
├── _config.yml           # Jekyll 配置
├── _layouts/             # 页面模板
│   ├── default.html      # 基础布局
│   ├── home.html         # 首页
│   └── post.html         # 文章页
├── _posts/               # 每日新闻 (YYYY-MM-DD-title.md)
├── _includes/            # 组件
│   ├── head.html
│   ├── header.html
│   └── footer.html
├── assets/               # 静态资源
│   ├── css/
│   └── js/
├── index.md              # 首页
└── about.md              # 关于页面
```

## 本地开发

```bash
# 安装 Jekyll
bundle install

# 本地预览
bundle exec jekyll serve

# 生成站点
bundle exec jekyll build
```

## 自动化流程

每天北京时间早8点：
1. 抓取各信源最新内容
2. AI分析整理精选资讯
3. 生成 Jekyll 文章
4. 推送到 GitHub Pages
5. 发送通知提醒

## License

MIT
