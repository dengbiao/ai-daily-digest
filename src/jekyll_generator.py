#!/usr/bin/env python3
"""
AI Daily Digest - Jekyll 网站生成器（文章流式版）
生成一篇连贯的精炼文章，而非卡片列表
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
        """生成文章 Markdown 内容 - 文章流式"""
        items = data.get('items', [])
        date_str = date.strftime('%Y年%m月%d日')
        
        lines = [
            '---',
            f'title: "AI日报 {date_str}"',
            f'date: {date.strftime("%Y-%m-%d %H:%M:%S")} +0800',
            'category: 日报',
            f'news_count: {len(items)}',
            '---',
            '',
            '<div class="article-container">',
            '',
            '<!-- 日报头部 -->',
            '<header class="article-header">',
            f'  <h1 class="article-title">AI日报 {date_str}</h1>',
            '  <div class="article-meta">',
            f'    <span>📅 {date_str}</span>',
            f'    <span>📊 {len(items)} 条精选资讯</span>',
            '  </div>',
            '</header>',
            '',
            '<!-- 导语 -->',
            '<p class="article-lead">',
            f'  今日AI领域共精选 {len(items)} 条重要资讯，涵盖',
        ]
        
        # 收集所有事件类型
        event_types = set()
        for item in items:
            event_types.add(item.get('event_type', '行业新闻'))
        event_type_names = list(event_types)[:3]
        lines.append(f'{"、".join(event_type_names)}等方面。以下是详细内容：')
        lines.append('</p>')
        lines.append('')
        
        # 生成文章正文 - 连贯的段落
        for i, item in enumerate(items, 1):
            lines.extend(self._generate_news_paragraph(item, i))
        
        # 页脚
        lines.extend([
            '',
            '<!-- 日报页脚 -->',
            '<footer class="article-footer">',
            '  <p>— 本文由 AI Daily Digest 自动生成 —</p>',
            '</footer>',
            '',
            '</div>',
        ])
        
        return '\n'.join(lines)
    
    def _generate_news_paragraph(self, item: dict, index: int) -> list:
        """生成单条新闻的段落 - 文章流式"""
        # 优先使用已翻译的内容
        if 'cn_title' in item and 'cn_summary' in item:
            cn_title = item['cn_title']
            cn_summary = item['cn_summary']
        else:
            event_type = item.get('event_type', '行业新闻')
            cn_title, cn_summary = self.cn_generator.translate_and_summarize(
                item['title'], 
                item['summary'],
                event_type
            )
        
        # 获取事件类型
        event_type = item.get('event_type', '行业新闻')
        event_label = self.cn_generator.get_event_type_label(event_type)
        
        # 获取来源链接
        sources = item.get('sources', [])
        source_name = sources[0]['name'] if sources else '原文'
        source_url = sources[0]['item_url'] if sources else '#'
        
        # 获取标签
        tags = item.get('tags', [])
        tags_text = ' '.join([f'#{tag}' for tag in tags[:2]]) if tags else ''
        
        lines = [
            f'<!-- 资讯 {index} -->',
            '<div class="news-section">',
            f'  <h2><span class="news-index">{index}.</span> {cn_title}</h2>',
            f'  <p>{cn_summary}</p>',
            '  <div class="news-source">',
            f'    <span class="source-tag">{event_label}</span>',
            f'    <a href="{source_url}" target="_blank" rel="noopener">{source_name} →</a>',
            f'    {tags_text}',
            '  </div>',
            '</div>',
            '',
        ]
        
        return lines


if __name__ == '__main__':
    with open('../data/digest.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    generator = JekyllGenerator()
    generator.generate(data)
