#!/usr/bin/env python3
"""
AI Daily Digest - 每日构建入口（OpenClaw 集成版）
协调抓取、分析、生成全流程，使用 OpenClaw 大模型翻译
"""

import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from fetcher import NewsFetcher
from analyzer import ContentAnalyzer
from jekyll_generator import JekyllGenerator
from openclaw_translator import OpenClawTranslator


def translate_with_openclaw(items: list) -> list:
    """使用 OpenClaw 大模型翻译"""
    print("\n【翻译】使用 OpenClaw 大模型翻译内容...")
    
    translator = OpenClawTranslator()
    items = translator.translate_batch(items)
    
    # 检查哪些需要翻译
    need_translation = [item for item in items if '_translation_prompt' in item]
    
    if not need_translation:
        print("  ✓ 所有内容已从缓存加载")
        return items
    
    print(f"  需要翻译: {len(need_translation)} 条")
    
    # 使用 OpenClaw 进行翻译
    for i, item in enumerate(need_translation, 1):
        print(f"  翻译 [{i}/{len(need_translation)}]: {item['title'][:40]}...")
        
        prompt = item['_translation_prompt']
        
        # 调用 OpenClaw 进行翻译
        try:
            # 使用 openclaw 命令行工具
            result = subprocess.run(
                ['openclaw', 'ask', prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                translated = result.stdout.strip()
                translator.apply_translation(item, translated)
                print(f"    ✓ 翻译完成")
            else:
                print(f"    ✗ 翻译失败，使用备用方案")
                # 使用备用翻译
                from chinese_generator import ChineseContentGenerator
                cg = ChineseContentGenerator()
                item['cn_title'], item['cn_summary'] = cg._smart_translate(
                    item['title'], item['summary']
                )
                
        except Exception as e:
            print(f"    ✗ 翻译出错: {e}")
            # 使用备用翻译
            from chinese_generator import ChineseContentGenerator
            cg = ChineseContentGenerator()
            item['cn_title'], item['cn_summary'] = cg._smart_translate(
                item['title'], item['summary']
            )
    
    print(f"  ✓ 翻译完成")
    return items


def main():
    """主流程"""
    print("=" * 50)
    print("AI Daily Digest - 每日构建 (OpenClaw 版)")
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
    
    # 转换为字典列表
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
                'related_urls': item.related_urls,
                'event_type': item.event_type
            }
            for item in digest_items
        ]
    }
    
    print(f"✓ 已生成精选 ({len(digest_items)} 条)")
    print()
    
    # 3. 翻译内容（使用 OpenClaw）
    digest_data['items'] = translate_with_openclaw(digest_data['items'])
    
    # 保存翻译后的数据
    with open(base_dir / 'data' / 'digest.json', 'w', encoding='utf-8') as f:
        json.dump(digest_data, f, ensure_ascii=False, indent=2)
    print()
    
    # 4. 生成 Jekyll 文章
    print("【步骤4】生成 Jekyll 文章...")
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
