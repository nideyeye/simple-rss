#!/usr/bin/env python
"""
订阅源创建功能测试脚本
测试创建订阅源后自动抓取文章的功能
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

from core.models import Category, Feed, Article
from core.services.fetcher import RSSFetcher
from core.services.parser import RSSParser


def test_real_rss_feed():
    """测试真实的 RSS 订阅源"""
    print("=" * 50)
    print("测试真实 RSS 订阅源")
    print("=" * 50)

    # 使用一个真实的 RSS 源
    test_url = 'https://www.djangoproject.com/rss/weblog/'

    print(f"\n测试订阅源: {test_url}")

    # 测试抓取
    fetcher = RSSFetcher()
    response = fetcher.fetch(test_url)

    if not response:
        print("✗ 抓取失败")
        return False

    print("✓ 抓取成功")

    # 测试解析
    parser = RSSParser()
    feed_data = parser.parse(response['content'], response['encoding'])

    if not feed_data:
        print("✗ 解析失败")
        return False

    print(f"✓ 解析成功")
    print(f"  - 标题: {feed_data['title']}")
    print(f"  - 描述: {feed_data['description'][:50]}...")
    print(f"  - 文章数: {len(feed_data['entries'])}")

    if feed_data['entries']:
        print(f"\n第一篇文章:")
        print(f"  - 标题: {feed_data['entries'][0]['title']}")
        print(f"  - 链接: {feed_data['entries'][0]['link']}")

    return True


def test_feed_creation():
    """测试订阅源创建和文章保存"""
    print("\n" + "=" * 50)
    print("测试订阅源创建")
    print("=" * 50)

    # 创建或获取分类
    category, _ = Category.objects.get_or_create(
        name='技术博客',
        defaults={'order': 1}
    )

    # 创建测试订阅源
    feed, created = Feed.objects.get_or_create(
        url='https://www.djangoproject.com/rss/weblog/',
        defaults={
            'title': 'Django 官方博客',
            'description': 'Django 框架官方博客',
            'category': category,
            'is_active': True,
        }
    )

    if created:
        print(f"✓ 创建新订阅源: {feed.title}")
    else:
        print(f"ℹ 订阅源已存在: {feed.title}")

    # 抓取文章
    fetcher = RSSFetcher()
    response = fetcher.fetch(feed.url)

    if not response:
        print("✗ 抓取失败")
        return False

    print("✓ 抓取成功")

    # 解析文章
    parser = RSSParser()
    feed_data = parser.parse(response['content'], response['encoding'])

    if not feed_data:
        print("✗ 解析失败")
        return False

    print(f"✓ 解析到 {len(feed_data['entries'])} 篇文章")

    # 保存文章
    new_count = 0
    for entry in feed_data['entries']:
        guid = entry.get('guid', entry['link'])
        if not Article.objects.filter(feed=feed, url=guid).exists():
            Article.objects.create(
                feed=feed,
                title=entry['title'] or '无标题',
                url=entry['link'],
                author=entry.get('author', ''),
                summary=entry.get('summary', ''),
                content=entry.get('content', ''),
                pub_date=entry.get('pub_date'),
            )
            new_count += 1

    print(f"✓ 保存了 {new_count} 篇新文章")

    # 统计文章总数
    total_articles = Article.objects.filter(feed=feed).count()
    print(f"✓ 订阅源共有 {total_articles} 篇文章")

    return True


def main():
    """主函数"""
    try:
        # 测试真实 RSS 源
        if not test_real_rss_feed():
            print("\n真实 RSS 源测试失败")
            return 1

        # 测试订阅源创建
        if not test_feed_creation():
            print("\n订阅源创建测试失败")
            return 1

        print("\n" + "=" * 50)
        print("所有测试通过！")
        print("=" * 50)
        print("\n提示:")
        print("  1. 访问 http://localhost:8000/feeds/ 查看订阅源列表")
        print("  2. 点击订阅源查看文章列表")
        print("  3. 访问 http://localhost:8000/admin/ 管理数据")
        return 0

    except Exception as e:
        print(f"\n✗ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
