#!/usr/bin/env python3
"""
AI Daily Digest - 智能中文内容生成器（Moonshot API 版）
使用 Moonshot Kimi 大模型进行高质量翻译
"""

import os
import re
import json
from typing import List, Dict, Tuple
from pathlib import Path


class ChineseContentGenerator:
    """智能中文内容生成器 - 使用 Moonshot API"""
    
    EVENT_TYPE_MAP = {
        '产品发布': '🚀 产品发布',
        '重大更新': '⚡ 重大更新',
        '公司动态': '🏢 公司动态',
        '开源发布': '🔓 开源发布',
        '合作投资': '🤝 合作投资',
        '行业新闻': '📰 行业新闻',
    }
    
    def __init__(self):
        self.cache = {}
        self.cache_file = Path(__file__).parent.parent / 'data' / 'translation_cache.json'
        self._load_cache()
        self._load_env()
    
    def _load_env(self):
        """加载环境变量"""
        env_file = Path(__file__).parent.parent / '.env'
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value
    
    def _load_cache(self):
        """加载翻译缓存"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
            except:
                self.cache = {}
    
    def _save_cache(self):
        """保存翻译缓存"""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"  缓存保存失败: {e}")
    
    def translate_and_summarize(self, title: str, summary: str, event_type: str = '行业新闻') -> Tuple[str, str]:
        """生成中文内容 - 优先使用 Moonshot API"""
        # 检查缓存
        cache_key = f"{title}|{summary[:80]}"
        if cache_key in self.cache:
            print(f"    [缓存命中]")
            return self.cache[cache_key]['title'], self.cache[cache_key]['summary']
        
        # 使用 Moonshot API 翻译
        cn_title, cn_summary = self._translate_with_moonshot(title, summary)
        
        # 保存到缓存
        self.cache[cache_key] = {'title': cn_title, 'summary': cn_summary}
        self._save_cache()
        
        return cn_title, cn_summary
    
    def _translate_with_moonshot(self, title: str, summary: str) -> Tuple[str, str]:
        """使用 Moonshot API 翻译"""
        try:
            from openai import OpenAI
            
            api_key = os.getenv('MOONSHOT_API_KEY')
            base_url = os.getenv('LLM_BASE_URL', 'https://api.moonshot.cn/v1')
            model = os.getenv('LLM_MODEL', 'kimi-k2.5')
            
            if not api_key:
                print("  [警告] 未配置 MOONSHOT_API_KEY，使用备用翻译")
                return self._fallback_translate(title, summary)
            
            client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
            
            prompt = f"""请将以下AI新闻标题和摘要翻译成地道的中文。

【原文标题】
{title}

【原文摘要】
{summary}

【翻译要求】
1. 标题12-18字，简洁有力，不要直译，要符合中文新闻标题习惯
2. 摘要60-90字，通顺易读，用中文表达习惯重新组织
3. 保留英文品牌名、产品名、人名（如OpenAI、ChatGPT、Claude、GitHub等）
4. 去除英文中的冗余信息，保留核心内容
5. 不要出现"详情请查看原文"这类敷衍内容

【输出格式】
标题：<中文标题>
摘要：<中文摘要>

【示例】
原文标题：OpenAI launches GPT-4 Turbo with 128K context window
原文摘要：OpenAI announces the release of GPT-4 Turbo featuring a 128K context window, allowing it to process about 300 pages of text in a single conversation.

标题：OpenAI发布GPT-4 Turbo：支持128K超长上下文
摘要：OpenAI推出新一代大模型GPT-4 Turbo，上下文窗口扩展至128K，可一次性处理约300页文本，同时API价格大幅降低。"""
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是专业的科技新闻编辑，擅长将英文科技新闻翻译成地道、简洁的中文。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=1.0,
                max_tokens=300
            )
            
            content = response.choices[0].message.content
            
            # 解析翻译结果
            title_match = re.search(r'标题[:：]\s*(.+?)(?:\n|$)', content)
            summary_match = re.search(r'摘要[:：]\s*(?:<[^>]+>)?\s*(.+?)(?:\n|$)', content, re.DOTALL)
            
            if title_match and summary_match:
                cn_title = title_match.group(1).strip()
                cn_summary = summary_match.group(1).strip()
                
                # 清理可能的多余内容
                cn_summary = cn_summary.split('\n')[0].strip()
                # 移除可能的 HTML 标签
                cn_summary = re.sub(r'<[^>]+>', '', cn_summary)
                
                return cn_title, cn_summary
            else:
                print(f"  [警告] API 返回格式异常，使用备用翻译")
                return self._fallback_translate(title, summary)
            
        except Exception as e:
            print(f"  [错误] Moonshot API 调用失败: {e}")
            return self._fallback_translate(title, summary)
    
    def _fallback_translate(self, title: str, summary: str) -> Tuple[str, str]:
        """备用翻译方案（API 失败时使用）"""
        # 提取公司名
        company = self._extract_company(title + ' ' + summary)
        
        # 简化标题
        words = title.split()[:5]
        simple_title = ' '.join(words)
        
        if company:
            cn_title = f"{company}：{simple_title}"
        else:
            cn_title = simple_title
        
        # 简化摘要
        if company:
            cn_summary = f"{company}发布重要更新，点击查看详情了解完整信息。"
        else:
            cn_summary = "点击查看原文了解详情。"
        
        return cn_title, cn_summary
    
    def _extract_company(self, text: str) -> str:
        """提取公司/产品名"""
        proper_nouns = {
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
            'chatgpt': 'ChatGPT',
            'claude': 'Claude',
            'gemini': 'Gemini',
            'copilot': 'Copilot',
        }
        
        text_lower = text.lower()
        for key, name in proper_nouns.items():
            if key in text_lower:
                return name
        return ''
    
    def get_event_type_label(self, event_type: str) -> str:
        return self.EVENT_TYPE_MAP.get(event_type, event_type)


# 批量翻译接口
def batch_translate(items: List[Dict]) -> List[Dict]:
    """批量翻译新闻条目"""
    generator = ChineseContentGenerator()
    
    for i, item in enumerate(items, 1):
        print(f"  翻译 [{i}/{len(items)}]: {item['title'][:40]}...")
        cn_title, cn_summary = generator.translate_and_summarize(
            item['title'],
            item['summary'],
            item.get('event_type', '行业新闻')
        )
        item['cn_title'] = cn_title
        item['cn_summary'] = cn_summary
    
    return items


if __name__ == '__main__':
    # 测试
    test_items = [
        {
            'title': 'Powering product discovery in ChatGPT',
            'summary': 'ChatGPT introduces richer, visually immersive shopping powered by the Agentic Commerce Protocol, enabling product discovery, side-by-side comparisons, and merchant integration.',
            'event_type': '产品发布'
        },
        {
            'title': 'OpenAI launches GPT-5 with multimodal capabilities',
            'summary': 'OpenAI announces the release of GPT-5, featuring advanced multimodal capabilities that allow users to interact with text, images, and audio in a single conversation.',
            'event_type': '产品发布'
        }
    ]
    
    results = batch_translate(test_items)
    for item in results:
        print(f"\n原标题: {item['title']}")
        print(f"中文标题: {item['cn_title']}")
        print(f"中文摘要: {item['cn_summary']}")
