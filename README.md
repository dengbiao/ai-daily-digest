# AI Daily Digest - 每日AI日报

一个自动抓取、整理并生成每日AI资讯的静态网站，托管于GitHub Pages。

## 特性

- 🤖 每日自动抓取AI领域最新资讯
- 📊 精选5-10条高质量信息
- 🔗 每条信息多源验证，可溯源
- 📱 响应式设计，适配各种设备
- 🎨 图文并茂，阅读体验佳
- ⏰ 每日早8点推送提醒

## 技术栈

- **生成器**: Python + Jinja2
- **样式**: Tailwind CSS
- **托管**: GitHub Pages
- **自动化**: GitHub Actions

## 目录结构

```
.
├── .github/workflows/     # GitHub Actions 工作流
├── src/                   # 源代码
│   ├── fetcher.py        # 信息抓取模块
│   ├── analyzer.py       # 内容分析模块
│   ├── generator.py      # 网页生成模块
│   └── templates/        # HTML模板
├── data/                  # 数据存储
│   └── sources.json      # 信源配置
├── docs/                  # 生成的网站
│   ├── index.html        # 主页
│   ├── archive/          # 历史归档
│   └── assets/           # 静态资源
└── scripts/              # 工具脚本
    └── daily_build.py    # 每日构建入口
```

## 信源

- AI新闻聚合平台
- 顶级AI实验室博客
- 知名AI研究者社交媒体
- 技术社区精选

## 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 生成日报
python scripts/daily_build.py

# 本地预览
cd docs && python -m http.server 8000
```

## 自动化流程

每天UTC时间0点（北京时间8点）自动运行：
1. 抓取各信源最新内容
2. AI分析整理精选资讯
3. 生成静态网页
4. 推送到GitHub Pages
5. 发送通知提醒

## License

MIT
