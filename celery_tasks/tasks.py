"""
Celery 定时任务定义
"""
import logging
from datetime import datetime, timedelta
from django.conf import settings
from celery import shared_task
from core.models import Feed, Article
from core.services.fetcher import RSSFetcher
from core.services.parser import RSSParser
from core.utils.article_utils import save_or_update_article

logger = logging.getLogger(__name__)


@shared_task
def fetch_all_feeds():
    """抓取所有启用的订阅源"""
    active_feeds = Feed.objects.filter(is_active=True)
    logger.info(f"开始抓取 {active_feeds.count()} 个订阅源")

    for feed in active_feeds:
        try:
            fetch_feed.delay(feed.pk)
        except Exception as e:
            logger.error(f"启动抓取任务失败 {feed.title}: {e}")


@shared_task
def fetch_feed(feed_id: int):
    """抓取单个订阅源"""
    try:
        feed = Feed.objects.get(pk=feed_id)
    except Feed.DoesNotExist:
        logger.error(f"订阅源不存在: {feed_id}")
        return

    logger.info(f"开始抓取订阅源: {feed.title}")

    # 抓取内容
    fetcher = RSSFetcher()
    response = fetcher.fetch(feed.url)

    if not response:
        feed.last_fetch_status = '抓取失败'
        feed.save()
        return

    # 解析内容
    parser = RSSParser()
    feed_data = parser.parse(response['content'], response['encoding'])

    if not feed_data:
        feed.last_fetch_status = '解析失败'
        feed.save()
        return

    # 更新订阅源信息
    if feed_data['title'] and feed_data['title'] != feed.title:
        feed.title = feed_data['title']
    if feed_data['description'] and not feed.description:
        feed.description = feed_data['description']

    feed.last_fetch_status = '成功'
    feed.last_fetch_at = datetime.now()
    feed.last_auto_fetch_at = datetime.now()
    feed.save()

    # 保存文章
    new_articles = 0
    for entry in feed_data['entries']:
        is_new, _ = save_or_update_article(feed, entry)
        if is_new:
            new_articles += 1

    logger.info(f"订阅源 {feed.title} 抓取完成，新增 {new_articles} 篇文章")


@shared_task
def cleanup_old_articles(days: int = 30):
    """清理旧文章"""
    cutoff_date = datetime.now() - timedelta(days=days)
    deleted_count = Article.objects.filter(created_at__lt=cutoff_date).delete()[0]
    logger.info(f"清理了 {deleted_count} 篇旧文章")


@shared_task
def translate_untranslated_articles(limit: int = 10):
    """翻译未翻译的文章（可选功能）"""
    # 这里可以根据需要实现自动翻译功能
    logger.info("翻译任务暂未实现")
