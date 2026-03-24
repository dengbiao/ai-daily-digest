#!/bin/bash
# AI Daily Digest - 本地构建并部署到 GitHub Pages

set -e

echo "=========================================="
echo "AI Daily Digest - 构建并部署"
echo "=========================================="
echo ""

# 检查是否在正确的目录
if [ ! -f "scripts/daily_build.py" ]; then
    echo "错误: 请在 ai-daily-digest 目录下运行此脚本"
    exit 1
fi

# 激活虚拟环境
echo "【1/5】激活虚拟环境..."
source venv/bin/activate

# 运行构建
echo "【2/5】构建日报..."
python3 scripts/daily_build.py

# 提交更改
echo "【3/5】提交更改到 Git..."
git add docs/_posts/ data/ src/ scripts/
git commit -m "Update: $(date +%Y-%m-%d) AI Daily Digest" || echo "没有需要提交的更改"

# 推送到 GitHub
echo "【4/5】推送到 GitHub..."
git push origin main

# 部署到 GitHub Pages
echo "【5/5】部署到 GitHub Pages..."
echo "  GitHub Actions 将自动构建并部署"
echo "  请访问 https://github.com/dengbiao/ai-daily-digest/actions 查看进度"

echo ""
echo "=========================================="
echo "完成!"
echo "网站地址: https://dengbiao.github.io/ai-daily-digest/"
echo "=========================================="
