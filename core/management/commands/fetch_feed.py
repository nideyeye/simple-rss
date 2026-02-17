"""
手动抓取订阅源管理命令
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Feed, Article
from core.services.fetcher import RSSFetcher
from core.services.parser import RSSParser
from core.utils.article_utils import save_or_update_article


class Command(BaseCommand):
    help = '手动抓取指定订阅源的文章'

    def add_arguments(self, parser):
        parser.add_argument(
            'feed_id',
            type=int,
            help='订阅源 ID',
        )
        parser.add_argument(
            '--timeout',
            type=int,
            default=30,
            help='抓取超时时间（秒），默认 30 秒',
        )

    def handle(self, *args, **options):
        feed_id = options['feed_id']
        timeout = options['timeout']

        try:
            feed = Feed.objects.get(pk=feed_id)
        except Feed.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'订阅源 ID {feed_id} 不存在'))
            return

        self.stdout.write(f'开始抓取订阅源: {feed.title}')
        self.stdout.write(f'URL: {feed.url}')
        self.stdout.write('=' * 80)

        # 抓取 RSS 内容
        fetcher = RSSFetcher()
        fetch_response = fetcher.fetch(feed.url, timeout=timeout)

        if not fetch_response:
            self.stdout.write(self.style.ERROR('抓取失败'))
            feed.last_fetch_status = '抓取失败'
            feed.last_fetch_at = timezone.now()
            feed.save()
            return

        self.stdout.write(self.style.SUCCESS(f'抓取成功 (状态码: {fetch_response["status_code"]})'))

        # 解析 RSS 内容
        parser = RSSParser()
        feed_data = parser.parse(fetch_response['content'], fetch_response['encoding'])

        if not feed_data:
            self.stdout.write(self.style.ERROR('解析失败'))
            feed.last_fetch_status = '解析失败'
            feed.last_fetch_at = timezone.now()
            feed.save()
            return

        self.stdout.write(self.style.SUCCESS(f'解析成功'))
        self.stdout.write(f'  - 标题: {feed_data["title"]}')
        self.stdout.write(f'  - 描述: {feed_data["description"][:100] if feed_data["description"] else "无"}...')
        self.stdout.write(f'  - 文章数: {len(feed_data["entries"])}')

        # 更新订阅源信息
        if feed_data['title'] and not feed.title:
            feed.title = feed_data['title']
        if feed_data['description'] and not feed.description:
            feed.description = feed_data['description']
        feed.last_fetch_status = '成功'
        feed.last_fetch_at = timezone.now()
        feed.save()

        # 保存文章
        new_count = 0
        for entry in feed_data['entries']:
            is_new, _ = save_or_update_article(feed, entry)
            if is_new:
                new_count += 1

        self.stdout.write('=' * 80)
        self.stdout.write(self.style.SUCCESS(f'抓取完成!'))
        self.stdout.write(f'  - 新增/更新文章: {new_count} 篇')
        self.stdout.write(f'  - 总文章数: {Article.objects.filter(feed=feed).count()} 篇')
