"""
核心数据模型
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid


class Category(models.Model):
    """文章分类"""
    name = models.CharField('分类名称', max_length=100, unique=True)
    slug = models.SlugField('URL标识', max_length=100, unique=True, blank=True)
    description = models.TextField('描述', blank=True)
    order = models.IntegerField('排序', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            # 对于中文等非 ASCII 字符，使用 UUID 作为 slug
            try:
                self.slug = slugify(self.name, allow_unicode=True)
                # 如果 slugify 返回空或非 ASCII，使用 UUID
                if not self.slug or not all(ord(c) < 128 for c in self.slug):
                    self.slug = str(uuid.uuid4())[:8]
            except:
                self.slug = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)


class Feed(models.Model):
    """RSS订阅源"""
    title = models.CharField('标题', max_length=200)
    url = models.URLField('订阅源地址', unique=True)
    description = models.TextField('描述', blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='分类',
        related_name='feeds'
    )
    is_active = models.BooleanField('是否启用', default=True)
    fetch_interval = models.IntegerField('抓取间隔（分钟）', default=60)
    last_fetch_at = models.DateTimeField('最后抓取时间', null=True, blank=True)
    last_auto_fetch_at = models.DateTimeField('最后自动刷新时间', null=True, blank=True)
    last_fetch_status = models.CharField('最后抓取状态', max_length=50, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '订阅源'
        verbose_name_plural = '订阅源'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Article(models.Model):
    """文章"""
    feed = models.ForeignKey(
        Feed,
        on_delete=models.CASCADE,
        verbose_name='订阅源',
        related_name='articles'
    )
    title = models.CharField('标题', max_length=500)
    url = models.URLField('文章链接')
    author = models.CharField('作者', max_length=200, blank=True)
    summary = models.TextField('摘要', blank=True)
    content = models.TextField('内容', blank=True)
    pub_date = models.DateTimeField('发布时间', null=True, blank=True)
    is_read = models.BooleanField('已读', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-pub_date']
        indexes = [
            models.Index(fields=['-pub_date']),
            models.Index(fields=['is_read']),
            models.Index(fields=['feed', '-pub_date']),
        ]

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    """用户配置"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户',
        related_name='rss_profile'
    )
    default_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='默认分类'
    )
    auto_read = models.BooleanField('自动标记已读', default=False)
    show_full_content = models.BooleanField('显示完整内容', default=False)
    items_per_page = models.IntegerField('每页显示数量', default=20)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户配置'
        verbose_name_plural = '用户配置'

    def __str__(self):
        return f"{self.user.username} 的配置"
