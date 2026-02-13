#!/usr/bin/env python
"""
数据库初始化脚本
创建示例分类和订阅源
"""
import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from core.models import Category, Feed
from django.contrib.auth.models import User


def init_categories():
    """初始化分类"""
    categories = [
        {'name': '技术博客', 'order': 1},
        {'name': '新闻资讯', 'order': 2},
        {'name': '开发工具', 'order': 3},
        {'name': '其他', 'order': 99},
    ]

    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'order': cat_data['order']}
        )
        if created:
            print(f"创建分类: {category.name}")


def init_sample_feeds():
    """初始化示例订阅源"""
    tech_category = Category.objects.filter(name='技术博客').first()

    sample_feeds = [
        {
            'title': 'Django Project',
            'url': 'https://www.djangoproject.com/rss/weblog/',
            'description': 'Django 官方博客',
            'category': tech_category,
        },
    ]

    for feed_data in sample_feeds:
        feed, created = Feed.objects.get_or_create(
            url=feed_data['url'],
            defaults=feed_data
        )
        if created:
            print(f"创建订阅源: {feed.title}")


def create_superuser():
    """创建超级用户（如果不存在）"""
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"创建超级用户: {username}")
        print(f"  邮箱: {email}")
        print(f"  密码: {password}")
        print("  请在生产环境中修改默认密码！")
    else:
        print(f"超级用户 {username} 已存在")


def main():
    """主函数"""
    print("开始初始化数据库...")

    init_categories()
    init_sample_feeds()
    create_superuser()

    print("数据库初始化完成！")
    print("\n请运行以下命令启动开发服务器:")
    print("  python manage.py runserver")
    print("\n访问管理后台:")
    print("  http://localhost:8000/admin/")


if __name__ == '__main__':
    main()
