#!/usr/bin/env python3
"""
AI Daily Digest - Jekyll 网站生成器（列表样式版）
生成中文 Jekyll 格式的文章和页面
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from chinese_generator import ChineseContentGenerator


class JekyllGenerator:
    """Jekyll 网站生成器"""
    
    def __init__(self, output_dir: str = 'docs'):
        self.output_dir = Path(output_dir)
        self.posts_dir = self.output_dir / '_posts'
        self.posts_dir.mkdir(parents=True, exist_ok=True)
        self.cn_generator = ChineseContentGenerator()
    
    def generate(self, digest_data: dict):
        """生成 Jekyll 文章"""
        print("Generating Jekyll posts with Chinese content...")
        
        today = datetime.now()
        date_str = today.strftime('%Y-%m-%d')
        
        # 生成文章文件名
        filename = f"{date_str}-ai-daily-digest.md"
        filepath = self.posts_dir / filename
        
        # 生成文章内容
        content = self._generate_post_content(digest_data, today)
        
        # 写入文件
        filepath.write_text(content, encoding='utf-8')
        print(f"  Generated: _posts/{filename}")
        
        print(f"\nJekyll site generated in {self.output_dir}")
        return filepath
    
    def _generate_post_content(self, data: dict, date: datetime) -> str:
        """生成文章 Markdown 内容 - 列表样式"""
        items = data.get('items', [])
        
        # Front Matter
        lines = [
            '---',
            f'title: "AI日报 {date.strftime("%Y年%m月%d日")}"',
            f'date: {date.strftime("%Y-%m-%d %H:%M:%S")} +0800',
            'category: 日报',
            f'news_count: {len(items)}',
            '---',
            '',
            '<!-- 日报头部 -->',
            '<div class="daily-header">',
            '  <div class="daily-meta">',
            f'    <span class="daily-count">{len(items)}</span>',
            '    <span class="daily-label">条精选资讯</span>',
            '  </div>',
            '  <p class="daily-desc">聚焦 AI 产品发布、公司动态、行业突破</p>',
            '</div>',
            '',
            '<!-- 新闻列表 -->',
            '<div class="news-list">',
            '',
        ]
        
        # 生成每条新闻
        for i, item in enumerate(items, 1):
            lines.extend(self._generate_news_section(item, i))
        
        lines.append('</div>')
        lines.append('')
        
        # 页脚
        lines.extend([
            '<!-- 日报页脚 -->',
            '<div class="daily-footer">',
            '  <p>🤖 AI Daily Digest · 每日追踪AI大事件</p>',
            '</div>',
        ])
        
        return '\n'.join(lines)
    
    def _generate_news_section(self, item: dict, index: int) -> list:
        """生成单条新闻的 Markdown - 列表样式"""
        # 优先使用已翻译的内容
        if 'cn_title' in item and 'cn_summary' in item:
            cn_title = item['cn_title']
            cn_summary = item['cn_summary']
        else:
            # 翻译标题和摘要
            event_type = item.get('event_type', '行业新闻')
            cn_title, cn_summary = self.cn_generator.translate_and_summarize(
                item['title'], 
                item['summary'],
                event_type
            )
        
        # 获取事件类型
        event_type = item.get('event_type', '行业新闻')
        event_label = self.cn_generator.get_event_type_label(event_type)
        importance = item['importance']
        
        # 热度等级
        if importance >= 9:
            heat_level = 'high'
        elif importance >= 7:
            heat_level = 'medium'
        else:
            heat_level = 'normal'
        
        # 获取来源链接
        sources = item.get('sources', [])
        source_html = ''
        if sources:
            source = sources[0]  # 只显示第一个来源
            source_html = f'<a href="{source["item_url"]}" target="_blank" rel="noopener" class="source-link">{source["name"]}</a>'
        
        # 获取标签
        tags = item.get('tags', [])
        tags_html = ''
        if tags:
            tags_html = ' '.join([f'<span class="tag">#{tag}</span>' for tag in tags[:3]])
        
        lines = [
            f'<!-- 新闻 {index} -->',
            f'<article class="news-item heat-{heat_level}">',
            '',
            '  <div class="news-header">',
            f'    <span class="news-number">{index:02d}</span>',
            f'    <span class="news-type">{event_label}</span>',
            '  </div>',
            '',
            f'  <h2 class="news-title"><a href="{sources[0]["item_url"] if sources else "#"}" target="_blank" rel="noopener">{cn_title}</a></h2>',
            '',
            f'  <p class="news-summary">{cn_summary}</p>',
            '',
            '  <div class="news-meta-row">',
            f'    {source_html}',
            f'    {tags_html}',
            '  </div>',
            '',
            '</article>',
            '',
        ]
        
        return lines


if __name__ == '__main__':
    with open('../data/digest.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    generator = JekyllGenerator()
    generator.generate(data)
