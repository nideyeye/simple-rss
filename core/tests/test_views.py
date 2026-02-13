"""
Core 应用视图测试
"""
from django.test import TestCase
from django.urls import reverse
from core.models import Category, Feed, Article


class FeedListViewTest(TestCase):
    """订阅源列表视图测试"""

    def setUp(self):
        """设置测试数据"""
        self.category = Category.objects.create(name='技术博客', order=1)
        self.feed = Feed.objects.create(
            title='测试订阅源',
            url='https://example.com/rss.xml',
            category=self.category,
            is_active=True
        )

    def test_feed_list_status_code(self):
        """测试订阅源列表页面状态码"""
        response = self.client.get(reverse('core:feed_list'))
        self.assertEqual(response.status_code, 200)

    def test_feed_list_template(self):
        """测试订阅源列表模板"""
        response = self.client.get(reverse('core:feed_list'))
        self.assertTemplateUsed(response, 'core/feed_list.html')


class ArticleListViewTest(TestCase):
    """文章列表视图测试"""

    def setUp(self):
        """设置测试数据"""
        self.category = Category.objects.create(name='技术博客', order=1)
        self.feed = Feed.objects.create(
            title='测试订阅源',
            url='https://example.com/rss.xml',
            category=self.category
        )
        self.article = Article.objects.create(
            feed=self.feed,
            title='测试文章',
            url='https://example.com/article/1'
        )

    def test_article_list_status_code(self):
        """测试文章列表页面状态码"""
        response = self.client.get(reverse('core:article_list'))
        self.assertEqual(response.status_code, 200)


class IndexViewTest(TestCase):
    """首页视图测试"""

    def test_index_status_code(self):
        """测试首页状态码"""
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)
