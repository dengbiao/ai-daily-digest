#!/usr/bin/env python3
"""
AI Daily Digest - LLM 翻译服务
通过 OpenClaw 子代理调用大模型进行翻译
"""

import json
import sys
import os
from typing import List, Dict, Tuple


class LLMTranslator:
    """使用 OpenClaw 内置大模型进行翻译"""
    
    def translate_batch(self, items: List[Dict]) -> List[Dict]:
        """批量翻译新闻条目"""
        results = []
        
        for item in items:
            cn_title, cn_summary = self.translate_single(
                item['title'],
                item['summary']
            )
            item['cn_title'] = cn_title
            item['cn_summary'] = cn_summary
            results.append(item)
        
        return results
    
    def translate_single(self, title: str, summary: str) -> Tuple[str, str]:
        """单条翻译 - 生成提示词供外部调用"""
        prompt = self._build_prompt(title, summary)
        return prompt
    
    def _build_prompt(self, title: str, summary: str) -> str:
        """构建翻译提示词"""
        return f"""请将以下AI新闻标题和摘要翻译成地道的中文。

【原文标题】
{title}

【原文摘要】
{summary}

【翻译要求】
1. 标题要简洁有力，12-18字，吸引点击，不要直译
2. 摘要要通顺易读，用中文表达习惯重新组织
3. 保留英文品牌名、产品名（如OpenAI、ChatGPT、Claude、GitHub等）
4. 去除冗余信息，保留核心内容
5. 摘要控制在60-100字

【输出格式】
标题：<中文标题>
摘要：<中文摘要>

【示例】
原文：OpenAI launches GPT-4 Turbo with 128K context window
标题：OpenAI发布GPT-4 Turbo：支持128K超长上下文
摘要：OpenAI推出新一代大模型GPT-4 Turbo，上下文窗口扩展至128K，可处理约300页文档，同时降低API价格。
"""


def translate_via_subagent(items: List[Dict]) -> List[Dict]:
    """
    通过子代理翻译 - 生成批量翻译任务
    返回需要翻译的条目列表
    """
    translator = LLMTranslator()
    
    # 准备翻译任务
    tasks = []
    for i, item in enumerate(items):
        prompt = translator._build_prompt(item['title'], item['summary'])
        tasks.append({
            'index': i,
            'title': item['title'],
            'prompt': prompt
        })
    
    return tasks


if __name__ == '__main__':
    # 测试模式
    test_items = [
        {
            'title': 'Powering product discovery in ChatGPT',
            'summary': 'ChatGPT introduces a new shopping experience powered by the Agentic Commerce Protocol, enabling users to discover and purchase products directly within the chat interface.',
            'event_type': '产品发布'
        },
        {
            'title': 'Building AI-powered GitHub issue triage with the Copilot SDK',
            'summary': 'Learn how to integrate the Copilot SDK into a React Native app to generate AI-powered issue summaries, with production-ready examples and best practices.',
            'event_type': '产品发布'
        }
    ]
    
    tasks = translate_via_subagent(test_items)
    for task in tasks:
        print(f"\n【{task['title']}】")
        print(task['prompt'])
        print("-" * 50)
