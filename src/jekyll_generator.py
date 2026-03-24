#!/usr/bin/env python3
"""
AI Daily Digest - Jekyll 网站生成器
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
        """生成文章 Markdown 内容"""
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
            '<div class="daily-intro">',
            f'  <p class="text-lg text-gray-300 mb-2">🔥 今日AI圈 <strong class="text-blue-400">{len(items)}</strong> 件大事</p>',
            '  <p class="text-sm text-gray-500">聚焦产品发布、公司动态、行业突破</p>',
            '</div>',
            '',
            '---',
            '',
        ]
        
        # 生成每条新闻
        for i, item in enumerate(items, 1):
            lines.extend(self._generate_news_section(item, i))
        
        # 页脚
        lines.extend([
            '',
            '---',
            '',
            '<div class="text-center text-gray-500 text-sm mt-8">',
            f'  <p>🤖 AI Daily Digest · 每日追踪AI大事件</p>',
            f'  <p class="mt-1">生成时间: {datetime.now().strftime("%H:%M")}</p>',
            '</div>',
        ])
        
        return '\n'.join(lines)
    
    def _generate_news_section(self, item: dict, index: int) -> list:
        """生成单条新闻的 Markdown"""
        # 翻译标题和摘要
        event_type = item.get('event_type', '行业新闻')
        cn_title, cn_summary = self.cn_generator.translate_and_summarize(
            item['title'], 
            item['summary'],
            event_type
        )
        
        # 事件类型和分类
        event_label = self.cn_generator.get_event_type_label(event_type)
        importance = item['importance']
        stars = '🔥' * (importance // 2)
        
        lines = [
            '',
            f'<article class="news-item my-8 p-6 bg-dark-surface rounded-xl border border-dark-border hover:border-blue-500/50 transition-all">',
            '',
            f'## <span class="text-blue-400">{index}.</span> {cn_title}',
            '',
            f'<div class="flex flex-wrap items-center gap-3 mb-4 text-sm">',
            f'  <span class="px-3 py-1 bg-gradient-to-r from-blue-500/20 to-purple-500/20 text-blue-400 rounded-full font-medium">{event_label}</span>',
            f'  <span class="text-orange-400">{stars}</span>',
            f'  <span class="text-gray-500">热度 {importance}/10</span>',
            f'</div>',
            '',
            f'<div class="prose prose-invert max-w-none">',
            f'  <p class="text-gray-300 leading-relaxed text-base">{cn_summary}</p>',
            f'</div>',
            '',
        ]
        
        # 信息源
        sources = item.get('sources', [])
        if sources:
            lines.append('<div class="mt-4">')
            lines.append('  <p class="text-sm text-gray-500 mb-2">📎 信息来源：</p>')
            lines.append('  <div class="flex flex-wrap gap-2">')
            for source in sources:
                lines.append(f'    <a href="{source["item_url"]}" target="_blank" rel="noopener" class="px-3 py-1.5 bg-dark-bg border border-dark-border rounded-lg text-sm text-gray-400 hover:text-blue-400 hover:border-blue-500/50 transition flex items-center gap-1">')
                lines.append(f'      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>')
                lines.append(f'      {source["name"]}')
                lines.append(f'    </a>')
            lines.append('  </div>')
            lines.append('</div>')
        
        # 标签
        tags = item.get('tags', [])
        if tags:
            lines.append('<div class="mt-4 flex flex-wrap gap-2">')
            for tag in tags[:4]:  # 最多4个标签
                lines.append(f'  <span class="px-2.5 py-1 bg-gray-800/80 text-gray-400 text-xs rounded-md border border-gray-700">{tag}</span>')
            lines.append('</div>')
        
        lines.append('')
        lines.append('</article>')
        lines.append('')
        
        return lines


if __name__ == '__main__':
    with open('../data/digest.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    generator = JekyllGenerator()
    generator.generate(data)
