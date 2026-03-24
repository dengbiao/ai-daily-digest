#!/usr/bin/env python3
"""
AI Daily Digest - 信息抓取模块
负责从各信源抓取最新内容
"""

import json
import feedparser
import requests
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from urllib.parse import urljoin
import time


@dataclass
class NewsItem:
    """新闻条目"""
    title: str
    url: str
    source: str
    source_url: str
    published: datetime
    summary: str
    content: str
    category: str
    tags: List[str]
    hash_id: str
    related_sources: List[Dict] = None
    
    def to_dict(self):
        data = asdict(self)
        data['published'] = self.published.isoformat()
        return data


class BaseFetcher:
    """基础抓取器"""
    
    def __init__(self, source_config: Dict):
        self.config = source_config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AI-Daily-Digest/1.0 (Research Bot)'
        })
    
    def fetch(self) -> List[NewsItem]:
        raise NotImplementedError
    
    def _generate_hash(self, text: str) -> str:
        """生成内容哈希用于去重"""
        return hashlib.md5(text.encode()).hexdigest()[:12]


class RSSFetcher(BaseFetcher):
    """RSS抓取器"""
    
    def fetch(self) -> List[NewsItem]:
        items = []
        try:
            feed = feedparser.parse(self.config['rss_url'])
            
            for entry in feed.entries[:10]:  # 每个源取前10条
                published = self._parse_date(entry)
                
                # 只取最近48小时的内容
                if datetime.now() - published > timedelta(hours=48):
                    continue
                
                item = NewsItem(
                    title=entry.get('title', ''),
                    url=entry.get('link', ''),
                    source=self.config['name'],
                    source_url=self.config['url'],
                    published=published,
                    summary=entry.get('summary', '')[:500],
                    content=entry.get('description', entry.get('summary', '')),
                    category=self.config.get('category', 'general'),
                    tags=[],
                    hash_id=self._generate_hash(entry.get('title', '') + entry.get('link', ''))
                )
                items.append(item)
                
        except Exception as e:
            print(f"Error fetching {self.config['name']}: {e}")
        
        return items
    
    def _parse_date(self, entry) -> datetime:
        """解析发布时间"""
        try:
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                return datetime(*entry.published_parsed[:6])
            if hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                return datetime(*entry.updated_parsed[:6])
        except:
            pass
        return datetime.now()


class PapersWithCodeFetcher(BaseFetcher):
    """Papers With Code API抓取器"""
    
    def fetch(self) -> List[NewsItem]:
        items = []
        try:
            # 获取最近的热门论文
            response = self.session.get(
                self.config['api_url'],
                params={'ordering': '-published', 'items_per_page': 10}
            )
            response.raise_for_status()
            data = response.json()
            
            for paper in data.get('results', []):
                published = datetime.fromisoformat(paper['published'].replace('Z', '+00:00'))
                
                if datetime.now() - published > timedelta(hours=48):
                    continue
                
                item = NewsItem(
                    title=paper['title'],
                    url=paper['url'],
                    source=self.config['name'],
                    source_url=self.config['url'],
                    published=published,
                    summary=paper.get('abstract', '')[:500],
                    content=paper.get('abstract', ''),
                    category='research',
                    tags=paper.get('tasks', []),
                    hash_id=self._generate_hash(paper['title'] + paper['url'])
                )
                items.append(item)
                
        except Exception as e:
            print(f"Error fetching {self.config['name']}: {e}")
        
        return items


class NewsFetcher:
    """新闻抓取管理器"""
    
    def __init__(self, sources_file: str):
        with open(sources_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
    
    def fetch_all(self) -> List[NewsItem]:
        """抓取所有信源"""
        all_items = []
        
        for source in self.config.get('sources', []):
            print(f"Fetching from {source['name']}...")
            
            fetcher = self._create_fetcher(source)
            if fetcher:
                items = fetcher.fetch()
                all_items.extend(items)
                print(f"  Got {len(items)} items")
            
            time.sleep(1)  # 礼貌延迟
        
        # 去重
        seen_hashes = set()
        unique_items = []
        for item in all_items:
            if item.hash_id not in seen_hashes:
                seen_hashes.add(item.hash_id)
                unique_items.append(item)
        
        print(f"\nTotal unique items: {len(unique_items)}")
        return unique_items
    
    def _create_fetcher(self, source: Dict) -> Optional[BaseFetcher]:
        """根据类型创建对应的抓取器"""
        source_type = source.get('type', 'rss')
        
        if source_type == 'rss':
            return RSSFetcher(source)
        elif source_type == 'api' and 'paperswithcode' in source.get('api_url', ''):
            return PapersWithCodeFetcher(source)
        # 可以扩展更多类型
        
        return None


if __name__ == '__main__':
    fetcher = NewsFetcher('data/sources.json')
    items = fetcher.fetch_all()
    
    # 保存原始数据
    output = {
        'fetched_at': datetime.now().isoformat(),
        'items': [item.to_dict() for item in items]
    }
    
    with open('data/raw_news.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved to data/raw_news.json")
