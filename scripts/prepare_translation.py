#!/usr/bin/env python3
"""
AI Daily Digest - 批量翻译脚本
使用 OpenClaw 内置大模型进行新闻翻译
"""

import json
import sys
import os
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from llm_translator import LLMTranslator


def load_digest():
    """加载需要翻译的摘要数据"""
    base_dir = Path(__file__).parent.parent
    digest_file = base_dir / 'data' / 'digest.json'
    
    with open(digest_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_translations(items):
    """保存翻译结果"""
    base_dir = Path(__file__).parent.parent
    output_file = base_dir / 'data' / 'translated.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({'items': items}, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 翻译结果已保存: {output_file}")


def main():
    """主函数 - 生成翻译任务文件"""
    print("=" * 50)
    print("AI Daily Digest - 翻译任务生成")
    print("=" * 50)
    
    # 加载数据
    data = load_digest()
    items = data.get('items', [])
    
    print(f"\n需要翻译的新闻条目: {len(items)} 条")
    
    # 生成翻译任务
    translator = LLMTranslator()
    tasks = []
    
    for i, item in enumerate(items):
        prompt = translator._build_prompt(item['title'], item['summary'])
        tasks.append({
            'index': i,
            'original_title': item['title'],
            'prompt': prompt
        })
    
    # 保存任务文件
    base_dir = Path(__file__).parent.parent
    tasks_file = base_dir / 'data' / 'translation_tasks.json'
    
    with open(tasks_file, 'w', encoding='utf-8') as f:
        json.dump({'tasks': tasks, 'count': len(tasks)}, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 翻译任务已生成: {tasks_file}")
    print(f"\n请运行以下命令进行翻译:")
    print(f"  openclaw run translate-tasks")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
