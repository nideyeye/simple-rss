"""
阅读器表单
"""
from django import forms
from .models import Favorite, ReadLater


class FavoriteForm(forms.ModelForm):
    """收藏表单"""

    class Meta:
        model = Favorite
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': '添加备注...'}),
        }


class ReadLaterForm(forms.ModelForm):
    """稍后阅读表单"""

    class Meta:
        model = ReadLater
        fields = []
