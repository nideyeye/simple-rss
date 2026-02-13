"""
RSS 抓取服务
"""
import logging
import requests
from typing import Optional, Dict, Any
from datetime import datetime
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


class RSSFetcher:
    """RSS订阅源抓取器"""

    def __init__(self, proxy_domain: Optional[str] = None):
        self.proxy_domain = proxy_domain or getattr(settings, 'CLOUDFLARE_PROXY_DOMAIN', None)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_proxy_url(self, url: str) -> str:
        """获取代理URL"""
        if self.proxy_domain:
            return f"{self.proxy_domain}/{url}"
        return url

    def fetch(self, feed_url: str, timeout: int = 30) -> Optional[Dict[str, Any]]:
        """
        抓取RSS订阅源

        Args:
            feed_url: 订阅源URL
            timeout: 超时时间（秒）

        Returns:
            包含响应数据的字典，或None（失败时）
        """
        try:
            url = self.get_proxy_url(feed_url)
            logger.info(f"正在抓取订阅源: {url}")

            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()

            return {
                'content': response.content,
                'encoding': response.encoding or 'utf-8',
                'url': response.url,
                'status_code': response.status_code,
                'headers': dict(response.headers),
            }

        except requests.exceptions.Timeout:
            logger.error(f"抓取超时: {feed_url}")
            return None

        except requests.exceptions.RequestException as e:
            logger.error(f"抓取失败 {feed_url}: {e}")
            return None

        except Exception as e:
            logger.exception(f"未知错误 {feed_url}: {e}")
            return None

    def fetch_multiple(self, urls: list, timeout: int = 30) -> Dict[str, Optional[Dict[str, Any]]]:
        """
        批量抓取多个订阅源

        Args:
            urls: URL列表
            timeout: 超时时间

        Returns:
            URL到响应数据的映射字典
        """
        results = {}
        for url in urls:
            results[url] = self.fetch(url, timeout)
        return results
