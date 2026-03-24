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
- 🌏 中文翻译，流畅阅读

## 技术栈

- **生成器**: Python + Jekyll
- **样式**: Tailwind CSS
- **翻译**: Moonshot API (Kimi)
- **托管**: GitHub Pages
- **自动化**: GitHub Actions

## 本地开发

### 安装依赖

```bash
python3 -m venv venv
source venv/bin/activate
pip install feedparser openai
```

### 配置 API Key

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 Moonshot API Key
```

### 构建日报

```bash
python3 scripts/daily_build.py
```

### 本地预览

```bash
cd docs
bundle install
bundle exec jekyll serve
```

## 自动部署

### 设置 GitHub Secrets

1. 进入 GitHub 仓库 Settings -> Secrets and variables -> Actions
2. 添加 `MOONSHOT_API_KEY` 密钥

### 自动构建

- **定时构建**: 每天北京时间早8点自动构建
- **手动触发**: 在 Actions 页面点击 "Run workflow"
- **推送触发**: 推送到 main 分支时自动部署

### 本地部署

```bash
./scripts/deploy.sh
```

## 目录结构

```
.
├── .github/workflows/    # GitHub Actions 配置
├── data/                 # 数据文件
│   ├── sources.json     # 信源配置
│   ├── raw_news.json    # 原始新闻数据
│   ├── digest.json      # 精选新闻
│   └── translation_cache.json  # 翻译缓存
├── docs/                # Jekyll 站点
│   ├── _posts/          # 每日文章
│   ├── _layouts/        # 页面模板
│   └── assets/          # 静态资源
├── scripts/             # 构建脚本
│   ├── daily_build.py   # 主构建脚本
│   └── deploy.sh        # 部署脚本
└── src/                 # Python 源码
    ├── fetcher.py       # 新闻抓取
    ├── analyzer.py      # 内容分析
    ├── chinese_generator.py  # 中文翻译
    └── jekyll_generator.py   # 文章生成
```

## License

MIT
