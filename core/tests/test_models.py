"""
Core 应用模型测试
"""
from django.test import TestCase
from core.models import Category, Feed, Article
from django.contrib.auth.models import User


class CategoryModelTest(TestCase):
    """Category 模型测试"""

    def test_create_category(self):
        """测试创建分类"""
        category = Category.objects.create(name='测试分类', order=1)
        self.assertEqual(category.name, '测试分类')
        # 中文分类使用 UUID 作为 slug
        self.assertIsNotNone(category.slug)
        self.assertEqual(str(category), '测试分类')


class FeedModelTest(TestCase):
    """Feed 模型测试"""

    def setUp(self):
        """设置测试数据"""
        self.category = Category.objects.create(name='技术博客', order=1)

    def test_create_feed(self):
        """测试创建订阅源"""
        feed = Feed.objects.create(
            title='测试订阅源',
            url='https://example.com/rss.xml',
            category=self.category
        )
        self.assertEqual(feed.title, '测试订阅源')
        self.assertEqual(str(feed), '测试订阅源')


class ArticleModelTest(TestCase):
    """Article 模型测试"""

    def setUp(self):
        """设置测试数据"""
        self.category = Category.objects.create(name='技术博客', order=1)
        self.feed = Feed.objects.create(
            title='测试订阅源',
            url='https://example.com/rss.xml',
            category=self.category
        )

    def test_create_article(self):
        """测试创建文章"""
        article = Article.objects.create(
            feed=self.feed,
            title='测试文章',
            url='https://example.com/article/1',
            summary='测试摘要'
        )
        self.assertEqual(article.title, '测试文章')
        self.assertEqual(str(article), '测试文章')
        self.assertFalse(article.is_read)
