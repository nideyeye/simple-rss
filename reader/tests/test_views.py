"""
Reader 应用视图测试
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Category, Feed, Article
from reader.models import Favorite, ReadLater


class FavoriteViewTest(TestCase):
    """收藏视图测试"""

    def setUp(self):
        """设置测试数据"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(self.user)
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

    def test_favorites_list_status_code(self):
        """测试收藏列表页面状态码"""
        response = self.client.get(reverse('reader:favorites'))
        self.assertEqual(response.status_code, 200)

    def test_add_favorite(self):
        """测试添加收藏"""
        response = self.client.post(
            reverse('reader:add_favorite', args=[self.article.pk])
        )
        self.assertEqual(Favorite.objects.count(), 1)


class ReadLaterViewTest(TestCase):
    """稍后阅读视图测试"""

    def setUp(self):
        """设置测试数据"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(self.user)
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

    def test_read_later_list_status_code(self):
        """测试稍后阅读列表页面状态码"""
        response = self.client.get(reverse('reader:read_later'))
        self.assertEqual(response.status_code, 200)

    def test_add_read_later(self):
        """测试添加稍后阅读"""
        response = self.client.post(
            reverse('reader:add_read_later', args=[self.article.pk])
        )
        self.assertEqual(ReadLater.objects.count(), 1)
