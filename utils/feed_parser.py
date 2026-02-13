"""
Feed 解析工具
提供 RSS/Atom 订阅源的解析功能
"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import feedparser

logger = logging.getLogger(__name__)


def parse_feed_url(url: str) -> Optional[Dict[str, Any]]:
    """
    从 URL 解析 Feed 信息

    Args:
        url: Feed URL

    Returns:
        解析后的 Feed 信息字典
    """
    try:
        parsed = feedparser.parse(url)

        if parsed.get('bozo') and parsed.get('bozo_exception'):
            logger.warning(f"Feed 解析警告: {parsed['bozo_exception']}")

        return {
            'title': parsed.feed.get('title', '未知订阅源'),
            'description': parsed.feed.get('description', ''),
            'link': parsed.feed.get('link', ''),
            'entries_count': len(parsed.entries),
        }

    except Exception as e:
        logger.exception(f"解析 Feed 失败: {e}")
        return None


def parse_feed_content(content: bytes, encoding: str = 'utf-8') -> Optional[Dict[str, Any]]:
    """
    解析 Feed 内容

    Args:
        content: Feed 内容字节流
        encoding: 内容编码

    Returns:
        解析后的数据字典
    """
    try:
        # 解码内容
        if isinstance(content, bytes):
            content_str = content.decode(encoding, errors='ignore')
        else:
            content_str = content

        parsed = feedparser.parse(content_str)

        return {
            'feed': {
                'title': parsed.feed.get('title', ''),
                'description': parsed.feed.get('description', ''),
                'link': parsed.feed.get('link', ''),
            },
            'entries': [
                {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('description', ''),
                    'summary': entry.get('summary', ''),
                    'content': _get_content(entry),
                    'author': entry.get('author', ''),
                    'published': _parse_date(entry.get('published_parsed')),
                    'updated': _parse_date(entry.get('updated_parsed')),
                    'guid': entry.get('id', entry.get('link', '')),
                }
                for entry in parsed.entries
            ],
        }

    except Exception as e:
        logger.exception(f"解析 Feed 内容失败: {e}")
        return None


def _get_content(entry: Dict) -> str:
    """提取文章内容"""
    if 'content' in entry:
        content_list = entry.get('content', [])
        if content_list and isinstance(content_list[0], dict):
            return content_list[0].get('value', '')

    return entry.get('summary', entry.get('description', ''))


def _parse_date(date_tuple) -> Optional[datetime]:
    """解析日期元组"""
    if date_tuple:
        try:
            return datetime(*date_tuple[:6])
        except (TypeError, ValueError):
            pass
    return None


def detect_feed_type(content: bytes) -> str:
    """
    检测 Feed 类型

    Args:
        content: Feed 内容

    Returns:
        Feed 类型（rss, atom, rdf, 或 unknown）
    """
    content_str = content.decode('utf-8', errors='ignore').lower()

    if '<rss' in content_str or '<rss:' in content_str:
        return 'rss'
    elif '<feed' in content_str or '<atom:' in content_str:
        return 'atom'
    elif '<rdf:' in content_str:
        return 'rdf'
    else:
        return 'unknown'
