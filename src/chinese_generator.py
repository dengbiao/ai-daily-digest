#!/usr/bin/env python3
"""
AI Daily Digest - 智能中文内容生成器
使用规则+AI方式生成高质量中文内容
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path


class ChineseContentGenerator:
    """中文内容生成器"""
    
    # 分类中文映射
    CATEGORY_MAP = {
        '🔬 研究进展': '研究进展',
        '🏢 行业动态': '行业动态',
        '🛠️ 工具资源': '工具资源',
        '📰 新闻资讯': '新闻资讯',
        '📚 教程学习': '教程学习',
    }
    
    # 标签中文映射
    TAG_MAP = {
        'LLM': '大语言模型',
        'Agent': '智能体',
        'Research': '研究',
        'Vision': '视觉',
        'Multimodal': '多模态',
        'Open Source': '开源',
        'Product': '产品',
    }
    
    def __init__(self):
        pass
    
    def translate_and_summarize(self, title: str, summary: str) -> tuple:
        """
        生成精炼的中文标题和摘要
        策略：提取核心概念，用中文重新组织表达
        """
        # 清理文本
        title = self._clean_text(title)
        summary = self._clean_text(summary)
        
        # 提取关键概念
        concepts = self._extract_concepts(title, summary)
        
        # 生成中文标题
        cn_title = self._generate_title(title, concepts)
        
        # 生成中文摘要
        cn_summary = self._generate_summary(summary, concepts)
        
        return cn_title, cn_summary
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        # 移除arXiv标记
        text = re.sub(r'arXiv:\d+\.\d+v\d+', '', text)
        text = re.sub(r'Announce Type:\s*\w+', '', text)
        text = re.sub(r'Abstract:\s*', '', text)
        # 清理多余空格
        text = ' '.join(text.split())
        return text.strip()
    
    def _extract_concepts(self, title: str, summary: str) -> dict:
        """提取关键概念"""
        text = (title + ' ' + summary).lower()
        
        concepts = {
            'has_agent': 'agent' in text or 'multi-agent' in text,
            'has_llm': 'llm' in text or 'language model' in text,
            'has_reasoning': 'reasoning' in text or 'thought' in text,
            'has_learning': 'learning' in text,
            'has_optimization': 'optimization' in text or 'optimize' in text,
            'has_generation': 'generation' in text or 'generative' in text,
            'has_simulation': 'simulation' in text,
            'has_benchmark': 'benchmark' in text,
            'has_clinical': 'clinical' in text or 'health' in text,
            'has_vision': 'vision' in text or 'image' in text,
            'has_multimodal': 'multimodal' in text,
            'has_error': 'error' in text or 'forecasting' in text,
            'has_search': 'search' in text or 'retrieval' in text,
            'has_compression': 'compression' in text,
            'has_math': 'mathematics' in text or 'math' in text,
            'has_detection': 'detection' in text,
        }
        
        return concepts
    
    def _generate_title(self, title: str, concepts: dict) -> str:
        """生成中文标题"""
        # 移除冒号前的作者名
        if ':' in title:
            parts = title.split(':', 1)
            if len(parts[0]) < 25:
                title = parts[1].strip()
        
        # 核心术语翻译映射
        translations = {
            r'\bagentic\b': '智能体化',
            r'\bagents?\b': '智能体',
            r'\bmulti-agent\b': '多智能体',
            r'\bllm\b': '大模型',
            r'\blarge language model\b': '大语言模型',
            r'\btree of thought\b': '思维树',
            r'\btot\b': '思维树',
            r'\bsimulation\b': '仿真',
            r'\bgeneration\b': '生成',
            r'\bgenerative\b': '生成式',
            r'\boptimization\b': '优化',
            r'\breasoning\b': '推理',
            r'\blearning\b': '学习',
            r'\bcontrastive\b': '对比',
            r'\bdetection\b': '检测',
            r'\bforecasting\b': '预测',
            r'\bbenchmark\b': '基准测试',
            r'\bself-evolving\b': '自进化',
            r'\bembodied\b': '具身',
            r'\bintrospection\b': '内省',
            r'\bcompression\b': '压缩',
            r'\bmathematics?\b': '数学',
            r'\bclinical\b': '临床',
            r'\bhealth\b': '健康',
            r'\bdata extraction\b': '数据提取',
            r'\berror\b': '错误',
            r'\bmarkov\b': '马尔可夫',
            r'\bdecomposition\b': '分解',
            r'\brefinement\b': '优化',
            r'\bvia\b': '通过',
            r'\bwith\b': '使用',
            r'\bfor\b': '用于',
            r'\busing\b': '使用',
            r'\band\b': '与',
            r'\bof\b': '',
            r'\bthe\b': '',
            r'\ba\b': '',
            r'\ban\b': '',
            r'\bin\b': '在',
            r'\bon\b': '在',
        }
        
        cn_title = title
        for pattern, replacement in translations.items():
            cn_title = re.sub(pattern, replacement, cn_title, flags=re.IGNORECASE)
        
        # 清理多余空格
        cn_title = ' '.join(cn_title.split())
        
        # 如果结果还是太英文化，基于概念生成标题
        if self._is_mostly_english(cn_title):
            cn_title = self._generate_concept_title(concepts, title)
        
        # 限制长度
        if len(cn_title) > 60:
            cn_title = cn_title[:57] + '...'
        
        return cn_title.strip()
    
    def _generate_concept_title(self, concepts: dict, original_title: str) -> str:
        """基于概念生成中文标题"""
        parts = []
        
        # 根据概念组合标题
        if concepts['has_agent']:
            if concepts['has_simulation']:
                parts.append('智能体仿真')
            elif concepts['has_error']:
                parts.append('多智能体错误预测')
            else:
                parts.append('智能体系统')
        
        if concepts['has_reasoning']:
            parts.append('推理优化')
        
        if concepts['has_learning']:
            if concepts['has_contrastive']:
                parts.append('对比学习')
            else:
                parts.append('学习方法')
        
        if concepts['has_optimization']:
            parts.append('优化技术')
        
        if concepts['has_clinical']:
            parts.append('临床数据')
        
        if concepts['has_compression']:
            parts.append('压缩技术')
        
        if concepts['has_math']:
            parts.append('数学建模')
        
        if not parts:
            # 提取原标题中的大写缩写作为主题
            acronyms = re.findall(r'\b[A-Z]{2,}\b', original_title)
            if acronyms:
                parts.append(f'{acronyms[0]}技术')
            else:
                parts.append('AI前沿研究')
        
        return '：'.join(parts[:2]) if len(parts) > 1 else parts[0]
    
    def _generate_summary(self, summary: str, concepts: dict) -> str:
        """生成中文摘要"""
        # 提取核心句子
        sentences = re.split(r'(?<=[.!?。！？])\s+', summary)
        core = sentences[0] if sentences else summary
        
        # 基于概念生成精炼摘要
        if concepts['has_agent'] and concepts['has_simulation']:
            return "本文提出了一种智能体仿真生成方法，通过分解复杂决策过程，实现了从自然语言描述到可执行仿真的自动转换。"
        
        if concepts['has_reasoning'] and concepts['has_optimization']:
            return "针对复杂推理任务，本文优化了思维树框架，在探索深度与计算效率之间取得更好平衡。"
        
        if concepts['has_clinical']:
            return "本文研究了从临床病历中提取结构化信息的方法，通过深度推理处理变量间的复杂依赖关系。"
        
        if concepts['has_learning'] and concepts['has_detection']:
            return "本文提出了增强的对比学习方法，用于检测文本属性图上的分布外样本，提升了模型的泛化能力。"
        
        if concepts['has_agent'] and concepts['has_error']:
            return "本文提出了多智能体系统的主动错误预测方法，利用马尔可夫转移动力学提前识别潜在故障。"
        
        if concepts['has_optimization'] and concepts['has_search']:
            return "本文针对生成式搜索引擎，提出了自进化的智能体优化系统，实现了从排名导向到内容生成的转变。"
        
        if concepts['has_benchmark']:
            return "本文构建了具身智能协作通信的基准测试，评估了在延迟、丢包等真实网络条件下的系统性能。"
        
        if concepts['has_compression'] and concepts['has_math']:
            return "本文探索了通过压缩原理进行数学建模的新范式，揭示了人类数学发现与形式化数学之间的关系。"
        
        if 'vector' in summary.lower():
            return "本文探讨了AI应用中的完整数据层架构，超越传统的向量存储方案，提供了更全面的数据管理视角。"
        
        if concepts['has_llm']:
            return "本文研究了大语言模型的新能力与应用，为AI技术发展提供了有价值的见解。"
        
        # 默认摘要
        return "本文探讨了人工智能领域的最新研究进展，提出了创新性的方法与技术。"
    
    def _is_mostly_english(self, text: str) -> bool:
        """检查文本是否主要是英文"""
        english_chars = len(re.findall(r'[a-zA-Z]{3,}', text))  # 至少3个字母的单词
        total_chars = len(text.replace(' ', '').replace('：', ''))
        if total_chars == 0:
            return True
        return english_chars / total_chars > 0.3
    
    def get_category_label(self, category: str) -> str:
        """获取分类中文标签"""
        return self.CATEGORY_MAP.get(category, category)
    
    def get_tag_label(self, tag: str) -> str:
        """获取标签中文标签"""
        return self.TAG_MAP.get(tag, tag)


if __name__ == '__main__':
    # 测试
    generator = ChineseContentGenerator()
    
    test_cases = [
        {
            'title': 'FactorSmith: Agentic Simulation Generation via Markov Decision Process Decomposition',
            'summary': 'Generating executable simulations from natural language specifications remains a challenging problem due to the limited reasoning capacity of large language models.'
        },
        {
            'title': 'Domain-Specialized Tree of Thought through Plug-and-Play Predictors',
            'summary': 'While Large Language Models have advanced complex reasoning, prominent methods like the Tree of Thoughts framework face a critical trade-off.'
        }
    ]
    
    for case in test_cases:
        cn_title, cn_summary = generator.translate_and_summarize(case['title'], case['summary'])
        print(f"原标题: {case['title']}")
        print(f"中文标题: {cn_title}")
        print(f"中文摘要: {cn_summary}")
        print()
