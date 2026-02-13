"""
RSS 解析服务
"""
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import feedparser

logger = logging.getLogger(__name__)


class RSSParser:
    """RSS订阅源解析器"""

    def __init__(self):
        self.parser = feedparser

    def parse(self, content: bytes, encoding: str = 'utf-8') -> Optional[Dict[str, Any]]:
        """
        解析RSS内容

        Args:
            content: RSS内容字节流
            encoding: 内容编码

        Returns:
            解析后的数据字典，或None（失败时）
        """
        try:
            # 解码内容
            if isinstance(content, bytes):
                content_str = content.decode(encoding, errors='ignore')
            else:
                content_str = content

            # 解析RSS
            feed_data = self.parser.parse(content_str)

            # 检查解析是否成功
            if feed_data.get('bozo') and feed_data.get('bozo_exception'):
                logger.warning(f"RSS解析警告: {feed_data['bozo_exception']}")

            return {
                'title': self._get_feed_title(feed_data),
                'description': self._get_feed_description(feed_data),
                'link': self._get_feed_link(feed_data),
                'entries': self._parse_entries(feed_data),
            }

        except Exception as e:
            logger.exception(f"RSS解析失败: {e}")
            return None

    def _get_feed_title(self, feed_data: Dict) -> str:
        """获取订阅源标题"""
        return feed_data.get('feed', {}).get('title', '未知订阅源')

    def _get_feed_description(self, feed_data: Dict) -> str:
        """获取订阅源描述"""
        return feed_data.get('feed', {}).get('description', '')

    def _get_feed_link(self, feed_data: Dict) -> str:
        """获取订阅源链接"""
        return feed_data.get('feed', {}).get('link', '')

    def _parse_entries(self, feed_data: Dict) -> List[Dict[str, Any]]:
        """解析文章列表"""
        entries = []
        for entry in feed_data.get('entries', []):
            try:
                entries.append({
                    'title': entry.get('title', '无标题'),
                    'link': entry.get('link', ''),
                    'author': entry.get('author', ''),
                    'summary': self._clean_html(entry.get('summary', entry.get('description', ''))),
                    'content': self._extract_content(entry),
                    'pub_date': self._parse_date(entry.get('published_parsed')),
                    'guid': entry.get('id', entry.get('link', '')),
                })
            except Exception as e:
                logger.warning(f"解析文章失败: {e}")
                continue

        return entries

    def _extract_content(self, entry: Dict) -> str:
        """提取文章内容"""
        if 'content' in entry:
            # 优先使用content字段
            content_list = entry.get('content', [])
            if content_list and isinstance(content_list[0], dict):
                return self._clean_html(content_list[0].get('value', ''))

        # 回退到summary或description
        return self._clean_html(entry.get('summary', entry.get('description', '')))

    def _clean_html(self, html: str) -> str:
        """清理HTML内容"""
        # 可以添加更复杂的HTML清理逻辑
        # 这里只做简单处理
        return html.strip() if html else ''

    def _parse_date(self, date_tuple) -> Optional[datetime]:
        """解析日期"""
        if date_tuple:
            try:
                return datetime(*date_tuple[:6])
            except (TypeError, ValueError):
                pass
        return None
