"""
Reader 应用模型测试
"""
from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Category, Feed, Article
from reader.models import Favorite, ReadLater, ReadingStatus


class FavoriteModelTest(TestCase):
    """Favorite 模型测试"""

    def setUp(self):
        """设置测试数据"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
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

    def test_create_favorite(self):
        """测试创建收藏"""
        favorite = Favorite.objects.create(
            user=self.user,
            article=self.article,
            notes='测试备注'
        )
        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.article, self.article)
        self.assertEqual(favorite.notes, '测试备注')


class ReadLaterModelTest(TestCase):
    """ReadLater 模型测试"""

    def setUp(self):
        """设置测试数据"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
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

    def test_create_read_later(self):
        """测试创建稍后阅读"""
        read_later = ReadLater.objects.create(
            user=self.user,
            article=self.article
        )
        self.assertEqual(read_later.user, self.user)
        self.assertEqual(read_later.article, self.article)
