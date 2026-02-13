from django.contrib import admin
from .models import ReadingStatus, Favorite, ReadLater


@admin.register(ReadingStatus)
class ReadingStatusAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'is_read', 'read_at']
    list_filter = ['is_read', 'read_at']
    search_fields = ['user__username', 'article__title']
    date_hierarchy = 'read_at'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'article__title']
    date_hierarchy = 'created_at'


@admin.register(ReadLater)
class ReadLaterAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'article__title']
    date_hierarchy = 'created_at'
