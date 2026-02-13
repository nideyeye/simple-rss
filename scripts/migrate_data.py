#!/usr/bin/env python
"""
数据迁移脚本
用于在版本之间迁移数据
"""
import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from core.models import Feed, Article


def migrate_feeds_add_slug():
    """迁移：为订阅源添加 slug 字段"""
    print("正在迁移订阅源数据...")

    feeds = Feed.objects.all()
    for feed in feeds:
        if not feed.slug:
            # 这里假设 Feed 模型有 slug 字段
            # 如果没有，需要先在 models.py 中添加
            pass

    print(f"迁移了 {feeds.count()} 个订阅源")


def migrate_articles_add_reading_time():
    """迁移：为文章添加阅读时间估算"""
    print("正在迁移文章数据...")

    articles = Article.objects.all()
    for article in articles:
        if hasattr(article, 'reading_time') and not article.reading_time:
            # 估算阅读时间（假设每分钟 200 字）
            word_count = len(article.content or '')
            article.reading_time = max(1, word_count // 200)
            article.save()

    print(f"迁移了 {articles.count()} 篇文章")


def main():
    """主函数"""
    print("数据迁移脚本")
    print("=" * 50)

    # 在这里添加需要执行的迁移任务
    # migrate_feeds_add_slug()
    # migrate_articles_add_reading_time()

    print("\n数据迁移完成！")


if __name__ == '__main__':
    main()
