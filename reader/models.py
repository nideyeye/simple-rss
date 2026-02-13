"""
阅读器数据模型
"""
from django.db import models
from django.contrib.auth.models import User
from core.models import Article


class ReadingStatus(models.Model):
    """阅读状态"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户',
        related_name='reading_statuses'
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='文章',
        related_name='reading_statuses'
    )
    is_read = models.BooleanField('已读', default=False)
    read_at = models.DateTimeField('阅读时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '阅读状态'
        verbose_name_plural = '阅读状态'
        unique_together = ['user', 'article']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['user', '-read_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"


class Favorite(models.Model):
    """收藏"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户',
        related_name='favorites'
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='文章',
        related_name='favorites'
    )
    notes = models.TextField('备注', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
        unique_together = ['user', 'article']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"


class ReadLater(models.Model):
    """稍后阅读"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户',
        related_name='read_laters'
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='文章',
        related_name='read_laters'
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '稍后阅读'
        verbose_name_plural = '稍后阅读'
        unique_together = ['user', 'article']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"
