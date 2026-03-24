#!/usr/bin/env python3
"""
AI Daily Digest - 内容分析模块
使用AI分析新闻内容，精选高质量信息
"""

import json
import os
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass
import re


@dataclass
class DigestItem:
    """精选资讯条目"""
    title: str
    summary: str
    importance: int  # 1-10
    category: str
    sources: List[Dict]  # 多个信息源
    tags: List[str]
    related_urls: List[str]
    image_url: str = None


class ContentAnalyzer:
    """内容分析器"""
    
    # 关键词权重
    KEYWORD_WEIGHTS = {
        'breakthrough': 2,
        '开源': 1.5,
        'open source': 1.5,
        'release': 1.3,
        '发布': 1.3,
        'model': 1.2,
        '模型': 1.2,
        'paper': 1.1,
        '论文': 1.1,
        'benchmark': 1.2,
        'sota': 1.5,
        'state of the art': 1.5,
        'gpt': 1.3,
        'llm': 1.3,
        '大模型': 1.3,
        'agent': 1.2,
        '智能体': 1.2,
        'multimodal': 1.3,
        '多模态': 1.3,
        'reasoning': 1.2,
        '推理': 1.2,
    }
    
    # 分类映射
    CATEGORIES = {
        'research': '🔬 研究进展',
        'industry': '🏢 行业动态',
        'tools': '🛠️ 工具资源',
        'news': '📰 新闻资讯',
        'tutorial': '📚 教程学习',
    }
    
    def __init__(self):
        self.min_items = 5
        self.max_items = 10
    
    def analyze(self, items: List[Dict]) -> List[DigestItem]:
        """分析并精选资讯"""
        print(f"Analyzing {len(items)} items...")
        
        # 1. 计算重要性分数
        scored_items = []
        for item in items:
            score = self._calculate_importance(item)
            scored_items.append((item, score))
        
        # 2. 按分数排序
        scored_items.sort(key=lambda x: x[1], reverse=True)
        
        # 3. 合并相似内容（多源验证）
        merged = self._merge_similar(scored_items)
        
        # 4. 精选top items
        selected = merged[:self.max_items]
        
        # 5. 如果不够最少数量，放宽条件
        if len(selected) < self.min_items:
            print(f"Warning: Only {len(selected)} items selected, minimum is {self.min_items}")
        
        # 6. 转换为DigestItem
        digest_items = []
        for item_data, score in selected:
            digest_item = self._create_digest_item(item_data, score)
            digest_items.append(digest_item)
        
        print(f"Selected {len(digest_items)} items for digest")
        return digest_items
    
    def _calculate_importance(self, item: Dict) -> float:
        """计算内容重要性分数"""
        score = 5.0  # 基础分
        
        text = f"{item.get('title', '')} {item.get('summary', '')} {item.get('content', '')}"
        text_lower = text.lower()
        
        # 关键词加分
        for keyword, weight in self.KEYWORD_WEIGHTS.items():
            if keyword in text_lower:
                score += weight
        
        # 来源权重
        source_weight = item.get('weight', 1.0)
        score *= source_weight
        
        # 时效性加分（越新分越高）
        try:
            published = datetime.fromisoformat(item.get('published', '').replace('Z', '+00:00'))
            hours_old = (datetime.now() - published).total_seconds() / 3600
            if hours_old < 6:
                score += 2
            elif hours_old < 12:
                score += 1
        except:
            pass
        
        return min(score, 10)  # 最高10分
    
    def _merge_similar(self, scored_items: List[tuple]) -> List[tuple]:
        """合并相似内容，聚合多源信息"""
        merged = []
        used_indices = set()
        
        for i, (item1, score1) in enumerate(scored_items):
            if i in used_indices:
                continue
            
            # 寻找相似内容
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
            
            # 合并信息
            if len(similar_items) > 1:
                item1['related_sources'] = sources[1:]
                item1['sources'] = sources
                # 多源验证加分
                score1 += 0.5 * len(similar_items)
            
            merged.append((item1, score1))
            used_indices.add(i)
        
        # 重新排序
        merged.sort(key=lambda x: x[1], reverse=True)
        return merged
    
    def _is_similar(self, item1: Dict, item2: Dict) -> bool:
        """判断两条内容是否相似"""
        # 简单的标题相似度检查
        title1 = item1.get('title', '').lower()
        title2 = item2.get('url', '').lower()
        
        # 提取关键词
        words1 = set(re.findall(r'\w+', title1))
        words2 = set(re.findall(r'\w+', title2))
        
        if not words1 or not words2:
            return False
        
        # Jaccard相似度
        intersection = words1 & words2
        union = words1 | words2
        similarity = len(intersection) / len(union)
        
        return similarity > 0.5
    
    def _create_digest_item(self, item: Dict, score: float) -> DigestItem:
        """创建精选条目"""
        # 生成摘要
        summary = self._generate_summary(item)
        
        # 确定分类
        category = item.get('category', 'news')
        category_label = self.CATEGORIES.get(category, '📰 新闻资讯')
        
        # 提取标签
        tags = item.get('tags', [])
        if not tags:
            tags = self._extract_tags(item)
        
        # 收集相关链接
        related_urls = []
        if item.get('related_sources'):
            related_urls = [s['item_url'] for s in item['related_sources'] if s.get('item_url')]
        
        # 主信息源
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
            tags=tags[:5],  # 最多5个标签
            related_urls=related_urls
        )
    
    def _generate_summary(self, item: Dict) -> str:
        """生成精炼摘要"""
        content = item.get('content', '') or item.get('summary', '')
        
        # 清理HTML标签
        content = re.sub(r'<[^>]+>', '', content)
        
        # 限制长度
        if len(content) > 300:
            # 找句子边界
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
        """从内容中提取标签"""
        text = f"{item.get('title', '')} {item.get('summary', '')}"
        text_lower = text.lower()
        
        tags = []
        tag_keywords = {
            'LLM': ['llm', '大模型', 'language model', 'gpt', 'claude'],
            'Vision': ['vision', 'image', 'multimodal', '视觉', '图像'],
            'Agent': ['agent', '智能体', 'autonomous'],
            'Research': ['paper', '论文', 'research', 'study'],
            'Open Source': ['open source', 'github', '开源'],
            'Product': ['launch', 'release', '发布', '产品'],
        }
        
        for tag, keywords in tag_keywords.items():
            if any(kw in text_lower for kw in keywords):
                tags.append(tag)
        
        return tags


if __name__ == '__main__':
    # 测试
    with open('data/raw_news.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    analyzer = ContentAnalyzer()
    digest_items = analyzer.analyze(data['items'])
    
    # 保存分析结果
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
                'related_urls': item.related_urls
            }
            for item in digest_items
        ]
    }
    
    with open('data/digest.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved to data/digest.json")
