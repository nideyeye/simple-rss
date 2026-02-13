"""
核心表单
"""
from django import forms
from .models import Feed, Category


class FeedForm(forms.ModelForm):
    """订阅源表单"""

    class Meta:
        model = Feed
        fields = ['title', 'url', 'description', 'category', 'is_active', 'fetch_interval']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'url': forms.URLInput(attrs={'placeholder': 'https://example.com/rss.xml'}),
        }


class CategoryForm(forms.ModelForm):
    """分类表单"""

    class Meta:
        model = Category
        fields = ['name', 'description', 'order']
