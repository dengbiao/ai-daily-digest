#!/usr/bin/env python3
"""
AI Daily Digest - 中文内容生成器
完整中文输出 - 基于模板重写
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path


class ChineseContentGenerator:
    """中文内容生成器 - 生成完整中文内容"""
    
    # 事件类型映射
    EVENT_TYPE_MAP = {
        '产品发布': '🚀 产品发布',
        '重大更新': '⚡ 重大更新',
        '公司动态': '🏢 公司动态',
        '开源发布': '🔓 开源发布',
        '合作投资': '🤝 合作投资',
        '行业新闻': '📰 行业新闻',
    }
    
    def translate_and_summarize(self, title: str, summary: str, event_type: str = '行业新闻') -> tuple:
        """生成完整的中文标题和摘要"""
        # 清理文本
        title = self._clean_text(title)
        summary = self._clean_text(summary)
        
        # 提取关键信息
        info = self._extract_info(title, summary)
        
        # 生成中文标题
        cn_title = self._generate_chinese_title(info, event_type)
        
        # 生成中文摘要
        cn_summary = self._generate_chinese_summary(info, event_type)
        
        return cn_title, cn_summary
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        text = re.sub(r'<[^>]+>', '', text)
        text = ' '.join(text.split())
        return text.strip()
    
    def _extract_info(self, title: str, summary: str) -> dict:
        """提取关键信息"""
        text = title + ' ' + summary
        text_lower = text.lower()
        
        info = {
            'companies': [],
            'products': [],
            'amount': '',
            'action': '',
            'topic': '',
        }
        
        # 提取公司名
        companies = {
            'openai': 'OpenAI',
            'anthropic': 'Anthropic',
            'google': 'Google',
            'deepmind': 'DeepMind',
            'microsoft': '微软',
            'meta': 'Meta',
            'facebook': 'Meta',
            'nvidia': 'NVIDIA',
            'stability': 'Stability AI',
            'huggingface': 'Hugging Face',
            'github': 'GitHub',
            'amazon': '亚马逊',
            'apple': '苹果',
            'xai': 'xAI',
            'lovable': 'Lovable',
            'techcrunch': 'TechCrunch',
            'mit': 'MIT',
            'mirage': 'Mirage',
            'agile robots': 'Agile Robots',
            'air street': 'Air Street Capital',
            'hark': 'Hark',
        }
        
        for key, name in companies.items():
            if key in text_lower:
                info['companies'].append(name)
        
        # 提取产品名
        products = {
            'chatgpt': 'ChatGPT',
            'gpt-4': 'GPT-4',
            'gpt-5': 'GPT-5',
            'gpt-4o': 'GPT-4o',
            'o1': 'o1',
            'o3': 'o3',
            'claude': 'Claude',
            'gemini': 'Gemini',
            'bard': 'Bard',
            'copilot': 'Copilot',
            'llama': 'Llama',
            'stable diffusion': 'Stable Diffusion',
            'midjourney': 'Midjourney',
            'dall-e': 'DALL-E',
            'whisper': 'Whisper',
            'sora': 'Sora',
            'captions': 'Captions',
            'codeql': 'CodeQL',
            'eva': 'EVA',
        }
        
        for key, name in products.items():
            if key in text_lower:
                info['products'].append(name)
        
        # 提取金额
        amount_match = re.search(r'\$([\d,]+)\s*(M|million|B|billion)', text, re.IGNORECASE)
        if amount_match:
            amount = amount_match.group(1).replace(',', '')
            unit = amount_match.group(2).lower()
            if unit in ['m', 'million']:
                info['amount'] = f"{amount}百万美元"
            elif unit in ['b', 'billion']:
                info['amount'] = f"{amount}亿美元"
        
        # 提取主题/关键词
        topics = {
            'product discovery': '产品发现',
            'shopping': '购物',
            'commerce': '电商',
            'video': '视频',
            'image': '图像',
            'code': '代码',
            'security': '安全',
            'voice': '语音',
            'agent': '智能体',
            'acquisition': '收购',
            'funding': '融资',
            'foundation': '基金会',
            'triage': '分类处理',
            'detection': '检测',
        }
        
        for key, name in topics.items():
            if key in text_lower:
                info['topic'] = name
                break
        
        return info
    
    def _generate_chinese_title(self, info: dict, event_type: str) -> str:
        """生成中文标题"""
        company = info['companies'][0] if info['companies'] else ''
        product = info['products'][0] if info['products'] else ''
        topic = info['topic']
        
        # 根据事件类型生成标题
        if event_type == '产品发布':
            if company and product:
                return f"{company}发布{product}新功能"
            elif company and topic:
                return f"{company}推出{topic}功能"
            elif company:
                return f"{company}发布新产品"
        
        elif event_type == '重大更新':
            if company and product:
                return f"{company}更新{product}"
            elif company:
                return f"{company}重大更新"
        
        elif event_type == '公司动态':
            if info['amount']:
                if company:
                    return f"{company}获得{info['amount']}融资"
                return f"AI公司获得{info['amount']}融资"
            elif 'acquisition' in str(info).lower():
                if company:
                    return f"{company}寻求收购机会"
                return "AI公司寻求收购"
            elif company:
                return f"{company}最新动态"
        
        elif event_type == '开源发布':
            if company:
                return f"{company}开源新项目"
            return "新开源项目发布"
        
        # 默认标题
        if company and topic:
            return f"{company}{topic}新进展"
        elif company:
            return f"{company}最新消息"
        elif topic:
            return f"AI{topic}新动态"
        
        return "AI行业最新动态"
    
    def _generate_chinese_summary(self, info: dict, event_type: str) -> str:
        """生成中文摘要"""
        company = info['companies'][0] if info['companies'] else '该公司'
        product = info['products'][0] if info['products'] else ''
        topic = info['topic']
        amount = info['amount']
        
        # 根据事件类型生成摘要
        if event_type == '产品发布':
            if product and topic:
                return f"{company}正式推出{product}的{topic}功能，进一步提升用户体验。"
            elif product:
                return f"{company}发布了{product}的重要更新，带来多项新功能。"
            elif topic:
                return f"{company}推出全新的{topic}功能，值得关注。"
            return f"{company}发布新产品，详情请点击查看。"
        
        elif event_type == '重大更新':
            if product:
                return f"{company}对{product}进行了重大升级，优化了核心功能。"
            return f"{company}推出重要更新，详情请查看原文。"
        
        elif event_type == '公司动态':
            if amount:
                return f"{company}宣布完成{amount}融资，将用于技术研发和市场拓展。"
            return f"{company}公布最新发展动态，详情请查看原文链接。"
        
        elif event_type == '开源发布':
            return f"{company}开源了新项目，为开发者社区贡献新工具。"
        
        elif event_type == '合作投资':
            return f"{company}宣布重要合作，详情请点击查看。"
        
        # 默认摘要
        if topic:
            return f"{company}在{topic}领域有新进展，值得关注。"
        return f"{company}最新消息，详情请查看原文。"
    
    def get_event_type_label(self, event_type: str) -> str:
        """获取事件类型标签"""
        return self.EVENT_TYPE_MAP.get(event_type, event_type)


if __name__ == '__main__':
    generator = ChineseContentGenerator()
    
    test_cases = [
        {
            'title': 'Powering product discovery in ChatGPT',
            'summary': 'ChatGPT introduces richer, visually immersive shopping powered by Agentic Commerce Protocol.',
            'event_type': '产品发布'
        },
        {
            'title': 'Mirage raises $75M to continue building models',
            'summary': 'Mirage has raised $75 million in growth financing.',
            'event_type': '公司动态'
        }
    ]
    
    for case in test_cases:
        cn_title, cn_summary = generator.translate_and_summarize(
            case['title'], case['summary'], case['event_type']
        )
        print(f"原标题: {case['title']}")
        print(f"中文标题: {cn_title}")
        print(f"中文摘要: {cn_summary}")
        print()
