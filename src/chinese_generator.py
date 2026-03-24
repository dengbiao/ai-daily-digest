#!/usr/bin/env python3
"""
AI Daily Digest - 中文内容生成器
简洁直接，保留核心信息
"""

import re


class ChineseContentGenerator:
    """中文内容生成器"""
    
    EVENT_TYPE_MAP = {
        '产品发布': '🚀 产品发布',
        '重大更新': '⚡ 重大更新',
        '公司动态': '🏢 公司动态',
        '开源发布': '🔓 开源发布',
        '合作投资': '🤝 合作投资',
        '行业新闻': '📰 行业新闻',
    }
    
    # 公司名映射
    COMPANY_NAMES = {
        'openai': 'OpenAI',
        'anthropic': 'Anthropic',
        'google': 'Google',
        'deepmind': 'DeepMind',
        'microsoft': '微软',
        'meta': 'Meta',
        'github': 'GitHub',
        'nvidia': 'NVIDIA',
        'apple': '苹果',
        'amazon': '亚马逊',
        'lovable': 'Lovable',
        'mirage': 'Mirage',
        'air street': 'Air Street Capital',
        'agile robots': 'Agile Robots',
        'hark': 'Hark',
        'stability': 'Stability AI',
        'huggingface': 'Hugging Face',
    }
    
    def translate_and_summarize(self, title: str, summary: str, event_type: str = '行业新闻') -> tuple:
        """生成中文内容"""
        # 清理
        title = self._clean(title)
        summary = self._clean(summary)
        
        # 提取公司名
        company = self._extract_company(title + ' ' + summary)
        
        # 简化标题
        cn_title = self._simplify_title(title, company)
        
        # 简化摘要
        cn_summary = self._simplify_summary(summary, company)
        
        return cn_title, cn_summary
    
    def _clean(self, text: str) -> str:
        """清理文本"""
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'arXiv:\S+', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_company(self, text: str) -> str:
        """提取公司名"""
        text_lower = text.lower()
        for key, name in self.COMPANY_NAMES.items():
            if key in text_lower:
                return name
        return ''
    
    def _simplify_title(self, title: str, company: str) -> str:
        """简化标题"""
        # 移除常见前缀
        title = re.sub(r'^(Introducing|Announcing|Launching|Meet)\s+', '', title, flags=re.I)
        
        # 如果标题太长，取前半部分
        if len(title) > 50:
            title = title[:47] + '...'
        
        # 如果提取到了公司名但标题里没有，加上
        if company and company not in title:
            title = f"{company}: {title}"
        
        return title
    
    def _simplify_summary(self, summary: str, company: str) -> str:
        """简化摘要 - 取第一句核心内容"""
        # 分割句子
        sentences = re.split(r'[.!?。！？]\s+', summary)
        if not sentences:
            return "详情请查看原文。"
        
        # 取第一句
        first = sentences[0].strip()
        
        # 如果太短，取第二句
        if len(first) < 30 and len(sentences) > 1:
            first = sentences[1].strip()
        
        # 限制长度
        if len(first) > 120:
            first = first[:117] + '...'
        
        # 简单的词替换
        simple_replace = {
            'announces': '宣布',
            'launches': '推出',
            'releases': '发布',
            'introduces': '推出',
            'raises': '获得',
            'funding': '融资',
            'million': '百万',
            'billion': '十亿',
            'AI': 'AI',
            'artificial intelligence': '人工智能',
        }
        
        for en, cn in simple_replace.items():
            first = re.sub(r'\b' + re.escape(en) + r'\b', cn, first, flags=re.I)
        
        return first if first else "详情请查看原文。"
    
    def get_event_type_label(self, event_type: str) -> str:
        return self.EVENT_TYPE_MAP.get(event_type, event_type)
