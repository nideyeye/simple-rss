"""
核心视图
"""
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Feed, Article, Category


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
