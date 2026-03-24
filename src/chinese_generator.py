#!/usr/bin/env python3
"""
AI Daily Digest - 中文内容生成器
针对AI行业大事件优化
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path


class ChineseContentGenerator:
    """中文内容生成器 - 专注AI大事件"""
    
    # 分类中文映射
    CATEGORY_MAP = {
        '🔥 行业动态': '行业动态',
        '📰 新闻资讯': '新闻资讯',
        '🛠️ 工具资源': '工具资源',
    }
    
    # 事件类型映射
    EVENT_TYPE_MAP = {
        '产品发布': '🚀 产品发布',
        '重大更新': '⚡ 重大更新',
        '公司动态': '🏢 公司动态',
        '开源发布': '🔓 开源发布',
        '合作投资': '🤝 合作投资',
        '行业新闻': '📰 行业新闻',
    }
    
    # 公司/产品名称映射
    COMPANY_MAP = {
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
        'grok': 'Grok',
    }
    
    # 产品名称映射
    PRODUCT_MAP = {
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
        'embedding': 'Embedding',
    }
    
    def translate_and_summarize(self, title: str, summary: str, event_type: str = '行业新闻') -> tuple:
        """生成精炼的中文标题和摘要"""
        title = self._clean_text(title)
        summary = self._clean_text(summary)
        
        # 提取公司和产品信息
        companies = self._extract_companies(title + ' ' + summary)
        products = self._extract_products(title + ' ' + summary)
        
        # 生成中文标题
        cn_title = self._generate_title(title, companies, products, event_type)
        
        # 生成中文摘要
        cn_summary = self._generate_summary(summary, companies, products, event_type)
        
        return cn_title, cn_summary
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        text = re.sub(r'<[^>]+>', '', text)
        text = ' '.join(text.split())
        return text.strip()
    
    def _extract_companies(self, text: str) -> list:
        """提取公司名称"""
        text_lower = text.lower()
        companies = []
        for key, name in self.COMPANY_MAP.items():
            if key in text_lower:
                companies.append(name)
        return list(dict.fromkeys(companies))  # 去重
    
    def _extract_products(self, text: str) -> list:
        """提取产品名称"""
        text_lower = text.lower()
        products = []
        for key, name in self.PRODUCT_MAP.items():
            if key in text_lower:
                products.append(name)
        return list(dict.fromkeys(products))
    
    def _generate_title(self, title: str, companies: list, products: list, event_type: str) -> str:
        """生成中文标题"""
        # 移除常见的英文前缀
        title = re.sub(r'^(Introducing|Announcing|Launching|Meet)\s+', '', title, flags=re.IGNORECASE)
        
        # 提取核心内容
        if ':' in title:
            parts = title.split(':', 1)
            if len(parts[0]) < 30:
                title = parts[1].strip()
        
        # 翻译常见动词和名词
        translations = {
            r'\blaunch\b': '发布',
            r'\brelease\b': '发布',
            r'\bannounce\b': '宣布',
            r'\bintroduce\b': '推出',
            r'\bunveil\b': ' unveiled',
            r'\bupdate\b': '更新',
            r'\bupgrade\b': '升级',
            r'\bnew\b': '新',
            r'\bnow available\b': '现已上线',
            r'\bcoming soon\b': '即将推出',
        }
        
        cn_title = title
        for pattern, replacement in translations.items():
            cn_title = re.sub(pattern, replacement, cn_title, flags=re.IGNORECASE)
        
        # 如果公司有产品，构建"公司+产品+动作"格式
        if companies and products:
            company = companies[0]
            product = products[0]
            # 尝试提取动作
            action = self._extract_action(cn_title)
            if action:
                cn_title = f"{company}{product}{action}"
            else:
                cn_title = f"{company}发布{product}新功能"
        elif companies:
            company = companies[0]
            cn_title = f"{company}：{cn_title}"
        
        # 限制长度
        if len(cn_title) > 60:
            cn_title = cn_title[:57] + '...'
        
        return cn_title.strip()
    
    def _extract_action(self, text: str) -> str:
        """提取动作词"""
        actions = ['发布', '推出', '上线', '更新', '升级', '宣布', '开源']
        for action in actions:
            if action in text:
                return action
        return ''
    
    def _generate_summary(self, summary: str, companies: list, products: list, event_type: str) -> str:
        """生成中文摘要"""
        # 提取第一句
        sentences = re.split(r'(?<=[.!?。！？])\s+', summary)
        core = sentences[0] if sentences else summary
        
        # 限制长度
        if len(core) > 200:
            core = core[:197] + '...'
        
        # 根据事件类型生成摘要模板
        if event_type == '产品发布':
            if companies and products:
                return f"{companies[0]}正式发布了{products[0]}，{self._extract_key_point(core)}"
            elif companies:
                return f"{companies[0]}发布了新产品，{self._extract_key_point(core)}"
        
        elif event_type == '重大更新':
            if companies and products:
                return f"{companies[0]}对{products[0]}进行了重大更新，{self._extract_key_point(core)}"
            elif companies:
                return f"{companies[0]}推出重要更新，{self._extract_key_point(core)}"
        
        elif event_type == '公司动态':
            if companies:
                return f"{companies[0]}传来新动态，{self._extract_key_point(core)}"
        
        elif event_type == '开源发布':
            if companies:
                return f"{companies[0]}开源了新项目，{self._extract_key_point(core)}"
            else:
                return f"新的开源项目发布，{self._extract_key_point(core)}"
        
        # 默认摘要
        if companies:
            return f"{companies[0]}最新消息：{self._extract_key_point(core)}"
        
        return self._extract_key_point(core)
    
    def _extract_key_point(self, text: str) -> str:
        """提取核心要点"""
        # 简化处理，返回精炼版本
        text = re.sub(r'^\s*([Tt]he|[Aa]|[Aa]n)\s+', '', text)
        text = re.sub(r'\s+', ' ', text)
        
        # 限制长度
        if len(text) > 120:
            text = text[:117] + '...'
        
        return text.strip()
    
    def get_category_label(self, category: str) -> str:
        """获取分类中文标签"""
        return self.CATEGORY_MAP.get(category, category)
    
    def get_event_type_label(self, event_type: str) -> str:
        """获取事件类型标签"""
        return self.EVENT_TYPE_MAP.get(event_type, event_type)
    
    def get_tag_label(self, tag: str) -> str:
        """获取标签中文标签"""
        return tag  # 保持原样


if __name__ == '__main__':
    generator = ChineseContentGenerator()
    
    test_cases = [
        {
            'title': 'OpenAI launches GPT-4 Turbo with vision capabilities',
            'summary': 'OpenAI announced the launch of GPT-4 Turbo, a new version of their flagship model that includes vision capabilities and improved performance.',
            'event_type': '产品发布'
        },
        {
            'title': 'Anthropic raises $750M in new funding round',
            'summary': 'Anthropic has secured $750 million in additional funding, bringing the company\'s valuation to $18.4 billion.',
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
