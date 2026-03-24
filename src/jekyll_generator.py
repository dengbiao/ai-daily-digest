#!/usr/bin/env python3
"""
AI Daily Digest - Jekyll 网站生成器
生成 Jekyll 格式的文章和页面
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path


class JekyllGenerator:
    """Jekyll 网站生成器"""
    
    def __init__(self, output_dir: str = 'docs'):
        self.output_dir = Path(output_dir)
        self.posts_dir = self.output_dir / '_posts'
        self.posts_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(self, digest_data: dict):
        """生成 Jekyll 文章"""
        print("Generating Jekyll posts...")
        
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
            f'> 今日精选 **{len(items)}** 条AI领域高质量资讯',
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
            f'*Generated at {datetime.now().strftime("%H:%M")}*',
        ])
        
        return '\n'.join(lines)
    
    def _generate_news_section(self, item: dict, index: int) -> list:
        """生成单条新闻的 Markdown"""
        lines = [
            '',
            f'## {index}. {item["title"]}',
            '',
            f'**{item["category"]}** · 重要度: {"⭐" * (item["importance"] // 2)}',
            '',
            f'{item["summary"]}',
            '',
        ]
        
        # 信息源
        sources = item.get('sources', [])
        if sources:
            lines.append('**来源：**')
            for source in sources:
                lines.append(f'- [{source["name"]}]({source["item_url"]})')
            lines.append('')
        
        # 标签
        tags = item.get('tags', [])
        if tags:
            lines.append(f'**标签：** {" ".join([f"`{tag}`" for tag in tags])}')
            lines.append('')
        
        return lines


if __name__ == '__main__':
    # 测试
    with open('../data/digest.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    generator = JekyllGenerator()
    generator.generate(data)
