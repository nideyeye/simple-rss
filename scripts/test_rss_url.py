#!/usr/bin/env python
"""
RSS URL 测试脚本
在创建订阅源前测试 URL 是否可访问
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

import requests
from core.services.parser import RSSParser


def test_rss_url(url: str, timeout: int = 10):
    """
    测试 RSS URL 是否可访问

    Args:
        url: RSS 订阅源 URL
        timeout: 超时时间（秒）
    """
    print("=" * 80)
    print(f"测试订阅源: {url}")
    print("=" * 80)

    # 测试连接
    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        print(f"✓ 连接成功")
        print(f"  状态码: {response.status_code}")
        print(f"  内容长度: {len(response.content)} 字节")
        print(f"  编码: {response.encoding}")

        if response.status_code != 200:
            print(f"✗ 状态码不是 200，可能不是有效的订阅源")
            return False

    except requests.exceptions.Timeout:
        print(f"✗ 连接超时（超过 {timeout} 秒）")
        print(f"  建议：")
        print(f"    1. 检查网络连接")
        print(f"    2. 尝试增加超时时间")
        print(f"    3. 检查是否需要科学上网")
        return False

    except requests.exceptions.SSLError:
        print(f"✗ SSL 证书验证失败")
        print(f"  建议：")
        print(f"    1. 检查 URL 是否使用 HTTPS")
        print(f"    2. 尝试使用 HTTP")
        return False

    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return False

    # 测试解析
    try:
        parser = RSSParser()
        feed_data = parser.parse(response.content, response.encoding)

        if not feed_data:
            print(f"✗ RSS 解析失败")
            print(f"  可能原因：")
            print(f"    1. 不是标准的 RSS/Atom 格式")
            print(f"    2. 内容编码问题")
            return False

        print(f"\n✓ RSS 解析成功")
        print(f"  标题: {feed_data['title']}")
        print(f"  描述: {feed_data['description'][:100] if feed_data['description'] else '无'}...")
        print(f"  文章数: {len(feed_data['entries'])}")

        if feed_data['entries']:
            print(f"\n最新 3 篇文章:")
            for i, entry in enumerate(feed_data['entries'][:3], 1):
                print(f"  {i}. {entry['title'][:60]}")

        print(f"\n✓ 该订阅源可以正常使用！")
        return True

    except Exception as e:
        print(f"✗ 解析出错: {e}")
        return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python scripts/test_rss_url.py <RSS_URL> [timeout]")
        print("\n示例:")
        print("  python scripts/test_rss_url.py https://www.djangoproject.com/rss/weblog/")
        print("  python scripts/test_rss_url.py https://planet.python.org/rss20.xml 15")
        print("\n推荐的测试订阅源:")
        print("  - https://www.djangoproject.com/rss/weblog/")
        print("  - https://planet.python.org/rss20.xml")
        print("  - https://www.bbc.com/zhongwen/simp/index.xml")
        return 1

    url = sys.argv[1]
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    if test_rss_url(url, timeout):
        print(f"\n" + "=" * 80)
        print(f"测试通过！可以使用该 URL 创建订阅源。")
        print("=" * 80)
        return 0
    else:
        print(f"\n" + "=" * 80)
        print(f"测试失败，请检查 URL 或选择其他订阅源。")
        print("=" * 80)
        return 1


if __name__ == '__main__':
    sys.exit(main())
