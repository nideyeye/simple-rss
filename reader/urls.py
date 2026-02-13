"""
reader/urls.py
阅读器应用的URL配置
"""
from django.urls import path
from . import views

app_name = 'reader'

urlpatterns = [
    path('favorites/', views.favorites_list, name='favorites'),
    path('read-later/', views.read_later_list, name='read_later'),
    path('favorite/add/<int:article_id>/', views.add_favorite, name='add_favorite'),
    path('favorite/remove/<int:article_id>/', views.remove_favorite, name='remove_favorite'),
    path('read-later/add/<int:article_id>/', views.add_read_later, name='add_read_later'),
    path('read-later/remove/<int:article_id>/', views.remove_read_later, name='remove_read_later'),
    path('mark-read/<int:article_id>/', views.mark_as_read, name='mark_as_read'),
]
