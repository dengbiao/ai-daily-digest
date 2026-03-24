#!/usr/bin/env python3
"""
AI Daily Digest - 翻译任务生成器
生成翻译任务供 OpenClaw 批量处理
"""

import json
import sys
from pathlib import Path


def generate_translation_prompts():
    """生成翻译提示词文件"""
    base_dir = Path(__file__).parent.parent
    digest_file = base_dir / 'data' / 'digest.json'
    
    # 加载摘要数据
    with open(digest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    items = data.get('items', [])
    
    # 生成翻译任务
    tasks = []
    for i, item in enumerate(items, 1):
        prompt = f"""【翻译任务 {i}/{len(items)}】

原文标题：{item['title']}
原文摘要：{item['summary']}

请将以上内容翻译成中文：
1. 标题15字以内，简洁有力，不要直译
2. 摘要60-90字，通顺易读
3. 保留英文品牌名（OpenAI、ChatGPT、Claude、GitHub等）
4. 按此格式返回：
标题：xxx
摘要：xxx
"""
        tasks.append({
            'index': i,
            'title': item['title'],
            'prompt': prompt
        })
    
    # 保存任务文件
    tasks_file = base_dir / 'data' / 'translation_tasks.txt'
    with open(tasks_file, 'w', encoding='utf-8') as f:
        f.write(f"# AI Daily Digest - 翻译任务\n")
        f.write(f"# 共 {len(tasks)} 条新闻需要翻译\n")
        f.write(f"# 请将这些任务发送给 OpenClaw 进行翻译\n")
        f.write("=" * 50 + "\n\n")
        
        for task in tasks:
            f.write(task['prompt'])
            f.write("\n" + "-" * 50 + "\n\n")
    
    print(f"✓ 翻译任务已生成: {tasks_file}")
    print(f"  共 {len(tasks)} 条新闻")
    print(f"\n使用方法:")
    print(f"  1. 查看任务文件: cat {tasks_file}")
    print(f"  2. 将任务发送给 OpenClaw 翻译")
    print(f"  3. 保存翻译结果到: {base_dir}/data/translations.json")


if __name__ == '__main__':
    generate_translation_prompts()
