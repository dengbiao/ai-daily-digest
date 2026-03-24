# GitHub Pages 部署配置指南

## 1. 配置 GitHub Secrets

访问 GitHub 仓库设置页面：
https://github.com/dengbiao/ai-daily-digest/settings/secrets/actions

点击 "New repository secret" 按钮，添加以下密钥：

**Name**: `MOONSHOT_API_KEY`
**Value**: `sk-ETn7w3YGtLRa9L7LsP0gR546KZuQa3j9b5ZTDOpn1aOMg94N`

## 2. 启用 GitHub Pages

访问设置页面：
https://github.com/dengbiao/ai-daily-digest/settings/pages

**Source**: GitHub Actions

## 3. 验证部署

推送完成后，访问 Actions 页面查看部署状态：
https://github.com/dengbiao/ai-daily-digest/actions

## 4. 访问网站

部署完成后，访问：
https://dengbiao.github.io/ai-daily-digest/

## 自动部署触发条件

- ✅ 每天北京时间早上8点（UTC 0点）
- ✅ 推送到 main 分支时
- ✅ 手动触发（在 Actions 页面点击 "Run workflow"）
