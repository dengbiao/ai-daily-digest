#!/usr/bin/env python3
"""
AI Daily Digest - 每日构建入口
协调抓取、分析、生成全流程
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from fetcher import NewsFetcher
from analyzer import ContentAnalyzer
from jekyll_generator import JekyllGenerator


def main():
    """主流程"""
    print("=" * 50)
    print("AI Daily Digest - 每日构建")
    print("=" * 50)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    base_dir = Path(__file__).parent.parent
    
    # 1. 抓取新闻
    print("【步骤1】抓取新闻...")
    fetcher = NewsFetcher(base_dir / 'data' / 'sources.json')
    raw_items = fetcher.fetch_all()
    
    # 保存原始数据
    raw_data = {
        'fetched_at': datetime.now().isoformat(),
        'items': [item.to_dict() for item in raw_items]
    }
    with open(base_dir / 'data' / 'raw_news.json', 'w', encoding='utf-8') as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)
    print(f"✓ 已保存原始数据 ({len(raw_items)} 条)")
    print()
    
    # 2. 分析精选
    print("【步骤2】分析精选...")
    analyzer = ContentAnalyzer()
    digest_items = analyzer.analyze(raw_data['items'])
    
    digest_data = {
        'generated_at': datetime.now().isoformat(),
        'items': [
            {
                'title': item.title,
                'summary': item.summary,
                'importance': item.importance,
                'category': item.category,
                'sources': item.sources,
                'tags': item.tags,
                'related_urls': item.related_urls
            }
            for item in digest_items
        ]
    }
    with open(base_dir / 'data' / 'digest.json', 'w', encoding='utf-8') as f:
        json.dump(digest_data, f, ensure_ascii=False, indent=2)
    print(f"✓ 已生成精选 ({len(digest_items)} 条)")
    print()
    
    # 3. 生成 Jekyll 文章
    print("【步骤3】生成 Jekyll 文章...")
    generator = JekyllGenerator(output_dir=str(base_dir / 'docs'))
    post_path = generator.generate(digest_data)
    print(f"✓ 文章生成完成: {post_path.name}")
    print()
    
    print("=" * 50)
    print("构建完成!")
    print(f"文章位置: {post_path}")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
