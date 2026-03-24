#!/usr/bin/env python3
"""
AI Daily Digest - 内容分析模块
聚焦AI行业大事件：产品发布、公司动态、重大更新
"""

import json
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class DigestItem:
    """精选资讯条目"""
    title: str
    summary: str
    importance: int  # 1-10
    category: str
    sources: List[Dict]
    tags: List[str]
    related_urls: List[str]
    event_type: str  # 事件类型：产品发布/公司动态/重大更新/开源发布


class ContentAnalyzer:
    """内容分析器 - 专注AI大事件"""
    
    # 事件类型权重
    EVENT_WEIGHTS = {
        '产品发布': 3.0,
        '重大更新': 2.5,
        '公司动态': 2.0,
        '开源发布': 2.0,
        '合作投资': 1.8,
        '行业新闻': 1.5,
    }
    
    # 关键词权重 - 大事件相关
    KEYWORD_WEIGHTS = {
        # 产品动作
        'launch': 2.5, 'release': 2.5, 'announce': 2.0, 'introduce': 2.0,
        'unveil': 2.0, 'debut': 2.0, ' rollout': 2.0,
        '发布': 2.5, '推出': 2.5, '上线': 2.5, '更新': 1.5, '新版本': 2.0,
        'available now': 2.0, 'now live': 2.0, 'coming soon': 1.5,
        
        # 公司动态
        'acquisition': 2.0, 'merge': 2.0, 'partnership': 1.8,
        'funding': 1.8, 'investment': 1.8, 'ipo': 2.5,
        '收购': 2.0, '合并': 2.0, '融资': 1.8, '投资': 1.5, '上市': 2.5,
        '合作': 1.5, '战略': 1.5,
        
        # 开源
        'open source': 2.0, '开源': 2.0, 'github': 1.5,
        'free': 1.5, 'public': 1.5,
        
        # 重要产品
        'gpt-4': 2.0, 'gpt-5': 3.0, 'gpt-6': 3.0, 'chatgpt': 2.0,
        'claude': 2.0, 'gemini': 2.0, 'copilot': 2.0, 'llama': 2.0,
        'o1': 2.5, 'o3': 2.5, 'sonnet': 2.0, 'opus': 2.0,
        'stable diffusion': 1.8, 'midjourney': 1.8, 'dall-e': 1.8,
        
        # 重大特性
        'multimodal': 1.8, 'agent': 1.8, 'api': 1.5,
        '多模态': 1.8, '智能体': 1.8,
    }
    
    # 排除关键词 - 学术论文
    EXCLUDE_KEYWORDS = [
        'arxiv', 'paper', 'research paper', 'journal', 'conference',
        'study', 'experiment', 'experimental', 'evaluation',
        'dataset', 'benchmark', 'baseline', 'ablation',
        'appendix', 'supplementary', 'theorem', 'lemma',
        'proof', 'corollary', 'hypothesis', 'methodology',
        '论文', '研究', '实验', '基准测试', '消融实验',
    ]
    
    # 分类映射
    CATEGORIES = {
        '行业动态': '🔥 行业动态',
        '新闻资讯': '📰 新闻资讯',
        '工具资源': '🛠️ 工具资源',
    }
    
    def __init__(self):
        self.min_items = 5
        self.max_items = 10
    
    def analyze(self, items: List[Dict]) -> List[DigestItem]:
        """分析并精选资讯"""
        print(f"Analyzing {len(items)} items...")
        
        # 1. 过滤掉学术论文
        filtered_items = self._filter_academic_papers(items)
        print(f"  Filtered to {len(filtered_items)} non-academic items")
        
        # 2. 计算重要性分数
        scored_items = []
        for item in filtered_items:
            score, event_type = self._calculate_importance(item)
            item['event_type'] = event_type
            scored_items.append((item, score))
        
        # 3. 按分数排序
        scored_items.sort(key=lambda x: x[1], reverse=True)
        
        # 4. 合并相似内容
        merged = self._merge_similar(scored_items)
        
        # 5. 精选top items
        selected = merged[:self.max_items]
        
        # 6. 如果不够最少数量，提示
        if len(selected) < self.min_items:
            print(f"  Warning: Only {len(selected)} items selected, minimum is {self.min_items}")
        
        # 7. 转换为DigestItem
        digest_items = []
        for item_data, score in selected:
            digest_item = self._create_digest_item(item_data, score)
            digest_items.append(digest_item)
        
        print(f"  Selected {len(digest_items)} items for digest")
        return digest_items
    
    def _filter_academic_papers(self, items: List[Dict]) -> List[Dict]:
        """过滤掉学术论文"""
        filtered = []
        for item in items:
            text = f"{item.get('title', '')} {item.get('summary', '')}".lower()
            
            # 检查是否包含排除关键词
            is_academic = any(kw.lower() in text for kw in self.EXCLUDE_KEYWORDS)
            
            # 检查是否来自学术源
            source = item.get('source', '').lower()
            is_arxiv = 'arxiv' in source or 'arxiv' in text
            
            if not is_academic and not is_arxiv:
                filtered.append(item)
        
        return filtered
    
    def _calculate_importance(self, item: Dict) -> tuple:
        """计算内容重要性分数和事件类型"""
        score = 5.0  # 基础分
        
        text = f"{item.get('title', '')} {item.get('summary', '')}"
        text_lower = text.lower()
        
        # 关键词加分
        for keyword, weight in self.KEYWORD_WEIGHTS.items():
            if keyword.lower() in text_lower:
                score += weight
        
        # 来源权重
        source = item.get('source', '')
        source_weight = item.get('weight', 1.0)
        score *= source_weight
        
        # 判断事件类型
        event_type = self._detect_event_type(text_lower)
        if event_type in self.EVENT_WEIGHTS:
            score += self.EVENT_WEIGHTS[event_type]
        
        # 时效性加分
        try:
            published = datetime.fromisoformat(item.get('published', '').replace('Z', '+00:00'))
            hours_old = (datetime.now() - published).total_seconds() / 3600
            if hours_old < 6:
                score += 2
            elif hours_old < 12:
                score += 1
        except:
            pass
        
        return min(score, 10), event_type
    
    def _detect_event_type(self, text: str) -> str:
        """检测事件类型"""
        if any(k in text for k in ['launch', 'release', '发布', '推出', '上线', 'available']):
            return '产品发布'
        elif any(k in text for k in ['update', 'upgrade', '更新', '新版本', 'improve']):
            return '重大更新'
        elif any(k in text for k in ['acquisition', 'merge', 'funding', 'ipo', '收购', '合并', '融资', '上市']):
            return '公司动态'
        elif any(k in text for k in ['open source', '开源', 'github']):
            return '开源发布'
        elif any(k in text for k in ['partnership', 'collaboration', '合作', '战略']):
            return '合作投资'
        else:
            return '行业新闻'
    
    def _merge_similar(self, scored_items: List[tuple]) -> List[tuple]:
        """合并相似内容"""
        merged = []
        used_indices = set()
        
        for i, (item1, score1) in enumerate(scored_items):
            if i in used_indices:
                continue
            
            similar_items = [item1]
            sources = [{
                'name': item1.get('source', ''),
                'url': item1.get('source_url', ''),
                'item_url': item1.get('url', '')
            }]
            
            for j, (item2, score2) in enumerate(scored_items[i+1:], i+1):
                if j in used_indices:
                    continue
                
                if self._is_similar(item1, item2):
                    similar_items.append(item2)
                    sources.append({
                        'name': item2.get('source', ''),
                        'url': item2.get('source_url', ''),
                        'item_url': item2.get('url', '')
                    })
                    used_indices.add(j)
            
            if len(similar_items) > 1:
                item1['related_sources'] = sources[1:]
                item1['sources'] = sources
                score1 += 0.5 * len(similar_items)
            
            merged.append((item1, score1))
            used_indices.add(i)
        
        merged.sort(key=lambda x: x[1], reverse=True)
        return merged
    
    def _is_similar(self, item1: Dict, item2: Dict) -> bool:
        """判断两条内容是否相似"""
        title1 = item1.get('title', '').lower()
        title2 = item2.get('title', '').lower()
        
        words1 = set(re.findall(r'\w+', title1))
        words2 = set(re.findall(r'\w+', title2))
        
        if not words1 or not words2:
            return False
        
        intersection = words1 & words2
        union = words1 | words2
        similarity = len(intersection) / len(union)
        
        return similarity > 0.5
    
    def _create_digest_item(self, item: Dict, score: float) -> DigestItem:
        """创建精选条目"""
        summary = self._generate_summary(item)
        category = item.get('category', '新闻资讯')
        category_label = self.CATEGORIES.get(category, '📰 新闻资讯')
        tags = self._extract_tags(item)
        
        related_urls = []
        if item.get('related_sources'):
            related_urls = [s['item_url'] for s in item['related_sources'] if s.get('item_url')]
        
        sources = item.get('sources', [{
            'name': item.get('source', ''),
            'url': item.get('source_url', ''),
            'item_url': item.get('url', '')
        }])
        
        return DigestItem(
            title=item.get('title', ''),
            summary=summary,
            importance=int(score),
            category=category_label,
            sources=sources,
            tags=tags[:5],
            related_urls=related_urls,
            event_type=item.get('event_type', '行业新闻')
        )
    
    def _generate_summary(self, item: Dict) -> str:
        """生成精炼摘要"""
        content = item.get('content', '') or item.get('summary', '')
        content = re.sub(r'<[^>]+>', '', content)
        
        if len(content) > 300:
            sentences = re.split(r'(?<=[.!?。！？])\s+', content)
            summary = ''
            for sent in sentences:
                if len(summary) + len(sent) < 280:
                    summary += sent + ' '
                else:
                    break
            content = summary.strip()
        
        return content[:300]
    
    def _extract_tags(self, item: Dict) -> List[str]:
        """提取标签"""
        text = f"{item.get('title', '')} {item.get('summary', '')}"
        text_lower = text.lower()
        
        tags = []
        tag_keywords = {
            'OpenAI': ['openai', 'chatgpt', 'gpt-4', 'gpt-5'],
            'Anthropic': ['anthropic', 'claude'],
            'Google': ['google', 'gemini', 'bard'],
            'Microsoft': ['microsoft', 'copilot', 'azure'],
            'Meta': ['meta', 'llama', 'facebook'],
            '产品发布': ['launch', 'release', '发布', '推出'],
            '开源': ['open source', 'github', '开源'],
            '多模态': ['multimodal', '多模态', 'vision', 'image'],
            '智能体': ['agent', '智能体'],
        }
        
        for tag, keywords in tag_keywords.items():
            if any(kw in text_lower for kw in keywords):
                tags.append(tag)
        
        return tags


if __name__ == '__main__':
    with open('../data/raw_news.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    analyzer = ContentAnalyzer()
    digest_items = analyzer.analyze(data['items'])
    
    output = {
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
    
    with open('../data/digest.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved to data/digest.json")
