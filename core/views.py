"""
核心视图
"""
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import logging
from .models import Feed, Article, Category
from .forms import FeedForm
from .services.fetcher import RSSFetcher
from .services.parser import RSSParser
from .utils.article_utils import save_or_update_article

logger = logging.getLogger(__name__)


def index(request):
    """首页"""
    return render(request, 'core/index.html')


class FeedListView(ListView):
    """订阅源列表"""
    model = Feed
    template_name = 'core/feed_list.html'
    context_object_name = 'feeds'
    paginate_by = 20

    def get_queryset(self):
        return Feed.objects.filter(is_active=True).select_related('category')


class FeedCreateView(CreateView):
    """创建订阅源"""
    model = Feed
    form_class = FeedForm
    template_name = 'core/feed_form.html'
    success_url = reverse_lazy('core:feed_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = '添加'
        return context

    def form_valid(self, form):
        """表单验证通过后自动抓取文章"""
        response = super().form_valid(form)
        feed = self.object

        # 自动抓取文章（同步方式）
        try:
            from .services.fetcher import RSSFetcher
            from .services.parser import RSSParser
            import logging

            logger = logging.getLogger(__name__)

            # 抓取 RSS 内容（使用较短的超时时间）
            logger.info(f"开始抓取订阅源: {feed.url}")
            fetcher = RSSFetcher()
            fetch_response = fetcher.fetch(feed.url, timeout=10)  # 10 秒超时

            if fetch_response:
                logger.info(f"抓取成功: {feed.url}")

                # 解析 RSS 内容
                parser = RSSParser()
                feed_data = parser.parse(fetch_response['content'], fetch_response['encoding'])

                if feed_data:
                    logger.info(f"解析成功，找到 {len(feed_data['entries'])} 篇文章")

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

                    messages.success(
                        self.request,
                        f'订阅源 "{feed.title}" 创建成功！已抓取 {new_count} 篇文章。'
                    )
                else:
                    feed.last_fetch_status = '解析失败'
                    feed.save()
                    messages.warning(
                        self.request,
                        f'订阅源 "{feed.title}" 创建成功，但解析失败。请稍后手动抓取。'
                    )
            else:
                feed.last_fetch_status = '抓取失败'
                feed.last_fetch_at = timezone.now()
                feed.save()
                messages.warning(
                    self.request,
                    f'订阅源 "{feed.title}" 创建成功，但抓取失败。请检查 URL 是否正确。'
                )

        except Exception as e:
            import traceback
            logger.error(f"抓取订阅源失败: {feed.url}, 错误: {str(e)}")
            logger.error(traceback.format_exc())

            feed.last_fetch_status = f'错误: {str(e)[:50]}'
            feed.last_fetch_at = timezone.now()
            feed.save()

            messages.error(
                self.request,
                f'订阅源 "{feed.title}" 创建成功，但自动抓取出错：{str(e)}'
            )

        return response


class FeedDetailView(DetailView):
    """订阅源详情"""
    model = Feed
    template_name = 'core/feed_detail.html'
    context_object_name = 'feed'


class ArticleListView(ListView):
    """文章列表"""
    model = Article
    template_name = 'core/article_list.html'
    context_object_name = 'articles'
    paginate_by = 20

    def get_queryset(self):
        feed_id = self.kwargs.get('feed_id')
        if feed_id:
            return Article.objects.filter(feed_id=feed_id).select_related('feed')
        return Article.objects.all().select_related('feed')


class ArticleDetailView(DetailView):
    """文章详情"""
    model = Article
    template_name = 'core/article_detail.html'
    context_object_name = 'article'

    def get_object(self):
        obj = super().get_object()
        # 标记为已读
        obj.is_read = True
        obj.save()
        return obj


@require_http_methods(["POST"])
@csrf_exempt
def refresh_all_feeds(request):
    """手动刷新所有订阅源"""
    results = []
    active_feeds = Feed.objects.filter(is_active=True)

    for feed in active_feeds:
        try:
            # 抓取 RSS 内容
            fetcher = RSSFetcher()
            fetch_response = fetcher.fetch(feed.url, timeout=30)

            if not fetch_response:
                results.append({
                    'feed_id': feed.pk,
                    'feed_title': feed.title,
                    'status': 'error',
                    'message': '抓取失败'
                })
                feed.last_fetch_status = '抓取失败'
                feed.last_fetch_at = timezone.now()
                feed.save()
                continue

            # 解析 RSS 内容
            parser = RSSParser()
            feed_data = parser.parse(fetch_response['content'], fetch_response['encoding'])

            if not feed_data:
                results.append({
                    'feed_id': feed.pk,
                    'feed_title': feed.title,
                    'status': 'error',
                    'message': '解析失败'
                })
                feed.last_fetch_status = '解析失败'
                feed.last_fetch_at = timezone.now()
                feed.save()
                continue

            # 更新订阅源信息
            if feed_data['title'] and not feed.title:
                feed.title = feed_data['title']
            if feed_data['description'] and not feed.description:
                feed.description = feed_data['description']

            feed.last_fetch_status = '成功'
            feed.last_fetch_at = timezone.now()
            feed.save()

            # 保存文章
            new_articles = 0
            for entry in feed_data['entries']:
                is_new, _ = save_or_update_article(feed, entry)
                if is_new:
                    new_articles += 1

            results.append({
                'feed_id': feed.pk,
                'feed_title': feed.title,
                'status': 'success',
                'message': f'成功，新增 {new_articles} 篇文章'
            })
            logger.info(f"订阅源 {feed.title} 刷新完成，新增 {new_articles} 篇文章")

        except Exception as e:
            logger.error(f"刷新订阅源失败 {feed.title}: {str(e)}")
            results.append({
                'feed_id': feed.pk,
                'feed_title': feed.title,
                'status': 'error',
                'message': str(e)[:100]
            })
            feed.last_fetch_status = f'错误: {str(e)[:50]}'
            feed.last_fetch_at = timezone.now()
            feed.save()

    return JsonResponse({
        'success': True,
        'total': len(active_feeds),
        'results': results
    })
