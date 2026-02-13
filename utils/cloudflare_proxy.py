"""
CloudFlare 代理工具
用于通过 CloudFlare Worker 代理访问 RSS 订阅源
"""
from typing import Optional


def get_proxy_url(worker_domain: str, target_url: str) -> str:
    """
    获取 CloudFlare Worker 代理 URL

    Args:
        worker_domain: CloudFlare Worker 域名（如：https://your-worker.workers.dev）
        target_url: 目标订阅源 URL

    Returns:
        代理后的 URL
    """
    # 确保 worker_domain 不以斜杠结尾
    worker_domain = worker_domain.rstrip('/')

    # 移除 target_url 的协议头（如果有）
    if target_url.startswith('http://'):
        target_url = target_url[7:]
    elif target_url.startswith('https://'):
        target_url = target_url[8:]

    return f"{worker_domain}/{target_url}"


def is_cloudflare_worker_url(url: str) -> bool:
    """
    检查是否是 CloudFlare Worker URL

    Args:
        url: 待检查的 URL

    Returns:
        是否是 CloudFlare Worker URL
    """
    return 'workers.dev' in url or 'worker' in url.lower()


class CloudFlareProxy:
    """CloudFlare 代理客户端"""

    def __init__(self, worker_domain: str):
        self.worker_domain = worker_domain.rstrip('/')

    def get_url(self, target_url: str) -> str:
        """获取代理 URL"""
        return get_proxy_url(self.worker_domain, target_url)

    def is_enabled(self) -> bool:
        """检查代理是否启用"""
        return bool(self.worker_domain)
