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


class FeedCreateViewTest(TestCase):
    """创建订阅源视图测试"""

    def setUp(self):
        """设置测试数据"""
        self.category = Category.objects.create(name='技术博客', order=1)

    def test_feed_create_get(self):
        """测试创建订阅源页面 GET 请求"""
        response = self.client.get(reverse('core:feed_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/feed_form.html')

    def test_feed_create_post_valid(self):
        """测试创建订阅源 POST 请求（有效数据）"""
        feed_count = Feed.objects.count()
        response = self.client.post(reverse('core:feed_create'), {
            'title': '新订阅源',
            'url': 'https://example.com/new-rss.xml',
            'description': '这是一个新的订阅源',
            'category': self.category.pk,
            'is_active': True,
            'fetch_interval': 60,
        })
        self.assertEqual(response.status_code, 302)  # 重定向
        self.assertEqual(Feed.objects.count(), feed_count + 1)
        self.assertTrue(Feed.objects.filter(title='新订阅源').exists())

    def test_feed_create_post_invalid(self):
        """测试创建订阅源 POST 请求（无效数据）"""
        feed_count = Feed.objects.count()
        response = self.client.post(reverse('core:feed_create'), {
            'title': '',  # 标题为空，应该验证失败
            'url': 'not-a-valid-url',  # URL 格式错误
        })
        self.assertEqual(response.status_code, 200)  # 保持在表单页面
        self.assertEqual(Feed.objects.count(), feed_count)  # 没有创建新记录


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
