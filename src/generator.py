#!/usr/bin/env python3
"""
AI Daily Digest - 网页生成模块
生成响应式静态网页
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


class SiteGenerator:
    """网站生成器"""
    
    def __init__(self, template_dir: str = 'src/templates', output_dir: str = 'docs'):
        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)
        
        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'archive').mkdir(exist_ok=True)
        (self.output_dir / 'assets').mkdir(exist_ok=True)
        
        # 设置Jinja2环境
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        # 添加自定义过滤器
        self.env.filters['format_date'] = self._format_date
        self.env.filters['format_time'] = self._format_time
    
    def generate(self, digest_data: dict):
        """生成网站"""
        print("Generating website...")
        
        # 复制静态资源
        self._copy_assets()
        
        # 生成首页
        self._generate_index(digest_data)
        
        # 生成归档页面
        self._generate_archive(digest_data)
        
        # 更新历史归档
        self._update_history(digest_data)
        
        print(f"Website generated in {self.output_dir}")
    
    def _copy_assets(self):
        """复制静态资源"""
        # 创建CSS文件
        css_content = self._generate_css()
        (self.output_dir / 'assets' / 'style.css').write_text(css_content, encoding='utf-8')
        
        # 创建JS文件
        js_content = self._generate_js()
        (self.output_dir / 'assets' / 'app.js').write_text(js_content, encoding='utf-8')
    
    def _generate_index(self, data: dict):
        """生成首页"""
        template = self.env.get_template('index.html')
        
        today = datetime.now()
        
        html = template.render(
            title=f"AI Daily Digest - {today.strftime('%Y年%m月%d日')}",
            date=today,
            items=data.get('items', []),
            generated_at=data.get('generated_at', datetime.now().isoformat())
        )
        
        (self.output_dir / 'index.html').write_text(html, encoding='utf-8')
        print("  Generated: index.html")
    
    def _generate_archive(self, data: dict):
        """生成分类归档页面"""
        template = self.env.get_template('archive.html')
        
        # 按分类分组
        categories = {}
        for item in data.get('items', []):
            cat = item.get('category', '📰 其他')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)
        
        html = template.render(
            title="归档 - AI Daily Digest",
            categories=categories,
            date=datetime.now()
        )
        
        (self.output_dir / 'archive' / 'index.html').write_text(html, encoding='utf-8')
        print("  Generated: archive/index.html")
    
    def _update_history(self, data: dict):
        """更新历史记录"""
        history_file = self.output_dir / 'history.json'
        
        history = []
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        
        # 添加今日记录
        today_entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'title': f"AI日报 {datetime.now().strftime('%Y年%m月%d日')}",
            'item_count': len(data.get('items', [])),
            'categories': list(set(item.get('category', '📰 其他') for item in data.get('items', [])))
        }
        
        # 去重并限制数量
        history = [h for h in history if h['date'] != today_entry['date']]
        history.insert(0, today_entry)
        history = history[:30]  # 保留最近30天
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def _generate_css(self) -> str:
        """生成CSS样式"""
        return '''
/* AI Daily Digest - 响应式样式 */

:root {
    --primary: #3b82f6;
    --primary-dark: #2563eb;
    --secondary: #8b5cf6;
    --background: #0f172a;
    --surface: #1e293b;
    --surface-light: #334155;
    --text: #f1f5f9;
    --text-muted: #94a3b8;
    --border: #334155;
    --success: #22c55e;
    --warning: #f59e0b;
    --danger: #ef4444;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background: var(--background);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}

/* Header */
header {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-light) 100%);
    border-bottom: 1px solid var(--border);
    padding: 2rem 0;
    margin-bottom: 2rem;
}

header h1 {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

header .subtitle {
    color: var(--text-muted);
    margin-top: 0.5rem;
}

header .date {
    color: var(--text-muted);
    font-size: 0.9rem;
    margin-top: 0.25rem;
}

/* Navigation */
nav {
    background: var(--surface);
    padding: 1rem 0;
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
}

nav .container {
    display: flex;
    gap: 1.5rem;
    align-items: center;
}

nav a {
    color: var(--text-muted);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}

nav a:hover, nav a.active {
    color: var(--primary);
}

/* Main Content */
main {
    padding: 2rem 0;
}

/* News Items */
.news-grid {
    display: grid;
    gap: 1.5rem;
}

.news-item {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    transition: transform 0.2s, box-shadow 0.2s;
}

.news-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.news-item .category {
    display: inline-block;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--primary);
    margin-bottom: 0.75rem;
}

.news-item h2 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    line-height: 1.4;
}

.news-item h2 a {
    color: var(--text);
    text-decoration: none;
    transition: color 0.2s;
}

.news-item h2 a:hover {
    color: var(--primary);
}

.news-item .summary {
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.7;
    margin-bottom: 1rem;
}

.news-item .meta {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: center;
    font-size: 0.85rem;
    color: var(--text-muted);
}

.news-item .sources {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.news-item .source-tag {
    background: var(--surface-light);
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    color: var(--text-muted);
    text-decoration: none;
    transition: background 0.2s;
}

.news-item .source-tag:hover {
    background: var(--primary);
    color: white;
}

.news-item .tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.75rem;
}

.news-item .tag {
    background: rgba(59, 130, 246, 0.1);
    color: var(--primary);
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 500;
}

.news-item .importance {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
}

.news-item .importance-bar {
    width: 60px;
    height: 4px;
    background: var(--surface-light);
    border-radius: 2px;
    overflow: hidden;
}

.news-item .importance-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--success), var(--warning), var(--danger));
    border-radius: 2px;
}

/* Archive Page */
.category-section {
    margin-bottom: 2rem;
}

.category-section h3 {
    font-size: 1.1rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

/* Empty State */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--text-muted);
}

.empty-state svg {
    width: 64px;
    height: 64px;
    margin-bottom: 1rem;
    opacity: 0.5;
}

/* Footer */
footer {
    background: var(--surface);
    border-top: 1px solid var(--border);
    padding: 2rem 0;
    margin-top: 3rem;
    text-align: center;
    color: var(--text-muted);
    font-size: 0.9rem;
}

footer a {
    color: var(--primary);
    text-decoration: none;
}

/* Responsive */
@media (max-width: 768px) {
    header h1 {
        font-size: 1.5rem;
    }
    
    .news-item {
        padding: 1rem;
    }
    
    .news-item h2 {
        font-size: 1.1rem;
    }
    
    nav .container {
        gap: 1rem;
        font-size: 0.9rem;
    }
}

@media (max-width: 480px) {
    .container {
        padding: 0 0.75rem;
    }
    
    .news-item .meta {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }
}

/* Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.news-item {
    animation: fadeIn 0.5s ease-out;
}

/* Loading State */
.loading {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 4rem;
}

.loading::after {
    content: '';
    width: 40px;
    height: 40px;
    border: 3px solid var(--surface-light);
    border-top-color: var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

/* Scroll to top */
.scroll-top {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background: var(--primary);
    color: white;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.scroll-top.visible {
    opacity: 1;
    visibility: visible;
}

.scroll-top:hover {
    background: var(--primary-dark);
    transform: translateY(-2px);
}
'''
    
    def _generate_js(self) -> str:
        """生成JavaScript"""
        return '''
// AI Daily Digest - 交互功能

document.addEventListener('DOMContentLoaded', function() {
    // 滚动到顶部按钮
    const scrollTop = document.createElement('div');
    scrollTop.className = 'scroll-top';
    scrollTop.innerHTML = '↑';
    document.body.appendChild(scrollTop);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollTop.classList.add('visible');
        } else {
            scrollTop.classList.remove('visible');
        }
    });
    
    scrollTop.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    
    // 新闻项淡入动画
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.news-item').forEach(function(item) {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        item.style.transition = 'opacity 0.5s, transform 0.5s';
        observer.observe(item);
    });
});
'''
    
    def _format_date(self, value):
        """格式化日期"""
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value.replace('Z', '+00:00'))
            except:
                return value
        return value.strftime('%Y年%m月%d日')
    
    def _format_time(self, value):
        """格式化时间"""
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value.replace('Z', '+00:00'))
            except:
                return value
        return value.strftime('%H:%M')


if __name__ == '__main__':
    # 测试生成
    with open('data/digest.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    generator = SiteGenerator()
    generator.generate(data)
