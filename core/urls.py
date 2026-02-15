"""
core/urls.py
核心应用的URL配置
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('feeds/', views.FeedListView.as_view(), name='feed_list'),
    path('feeds/create/', views.FeedCreateView.as_view(), name='feed_create'),
    path('feeds/<int:pk>/', views.FeedDetailView.as_view(), name='feed_detail'),
    path('articles/', views.ArticleListView.as_view(), name='article_list'),
    path('articles/<int:feed_id>/', views.ArticleListView.as_view(), name='feed_articles'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
]
