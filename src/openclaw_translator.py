#!/usr/bin/env python3
"""
AI Daily Digest - OpenClaw 翻译集成
通过调用 OpenClaw 大模型进行高质量翻译
"""

import json
import os
import re
from typing import List, Dict, Tuple


class OpenClawTranslator:
    """使用 OpenClaw 内置大模型翻译"""
    
    def __init__(self):
        self.cache = {}
        self.cache_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'translation_cache.json')
        self._load_cache()
    
    def _load_cache(self):
        """加载翻译缓存"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
            except:
                self.cache = {}
    
    def _save_cache(self):
        """保存翻译缓存"""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def translate_batch(self, items: List[Dict]) -> List[Dict]:
        """批量翻译 - 生成任务文件供 OpenClaw 处理"""
        results = []
        
        for item in items:
            cache_key = f"{item['title']}|{item['summary'][:50]}"
            
            # 检查缓存
            if cache_key in self.cache:
                item['cn_title'] = self.cache[cache_key]['title']
                item['cn_summary'] = self.cache[cache_key]['summary']
            else:
                # 生成翻译提示
                item['_translation_prompt'] = self._build_prompt(item['title'], item['summary'])
                item['_cache_key'] = cache_key
            
            results.append(item)
        
        return results
    
    def _build_prompt(self, title: str, summary: str) -> str:
        """构建翻译提示词"""
        return f"""将以下AI新闻翻译成中文。

原文标题：{title}
原文摘要：{summary}

要求：
1. 标题15字以内，简洁有力
2. 摘要60-90字，通顺易读
3. 保留英文品牌名（OpenAI、ChatGPT等）
4. 按此格式返回：
标题：xxx
摘要：xxx"""
    
    def apply_translation(self, item: Dict, translated_text: str):
        """应用翻译结果"""
        # 解析翻译结果
        title_match = re.search(r'标题[:：]\s*(.+?)(?:\n|$)', translated_text)
        summary_match = re.search(r'摘要[:：]\s*(.+?)(?:\n|$)', translated_text)
        
        if title_match:
            item['cn_title'] = title_match.group(1).strip()
        else:
            item['cn_title'] = item['title']
        
        if summary_match:
            item['cn_summary'] = summary_match.group(1).strip()
        else:
            item['cn_summary'] = "点击查看详情。"
        
        # 保存到缓存
        if '_cache_key' in item:
            self.cache[item['_cache_key']] = {
                'title': item['cn_title'],
                'summary': item['cn_summary']
            }
            self._save_cache()
        
        # 清理临时字段
        item.pop('_translation_prompt', None)
        item.pop('_cache_key', None)
        
        return item


# 使用示例
def prepare_translation_tasks(items: List[Dict]) -> List[Dict]:
    """准备翻译任务"""
    translator = OpenClawTranslator()
    return translator.translate_batch(items)


if __name__ == '__main__':
    # 测试
    test_items = [
        {
            'title': 'Powering product discovery in ChatGPT',
            'summary': 'ChatGPT introduces richer shopping experience.',
            'event_type': '产品发布'
        }
    ]
    
    results = prepare_translation_tasks(test_items)
    for item in results:
        print(f"\n原标题: {item['title']}")
        if '_translation_prompt' in item:
            print(f"翻译提示:\n{item['_translation_prompt']}")
