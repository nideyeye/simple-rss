from django.contrib import admin
from .models import Feed, Article, Category


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'category', 'is_active', 'created_at', 'updated_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'url', 'description']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed', 'pub_date', 'is_read', 'created_at']
    list_filter = ['feed', 'is_read', 'pub_date', 'created_at']
    search_fields = ['title', 'content', 'summary']
    date_hierarchy = 'pub_date'
    ordering = ['-pub_date']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
