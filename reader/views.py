"""
阅读器视图
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.decorators.http import require_POST
from core.models import Article
from .models import Favorite, ReadLater, ReadingStatus


@login_required
def favorites_list(request):
    """收藏列表"""
    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related('article__feed').order_by('-created_at')
    return render(request, 'reader/favorites.html', {'favorites': favorites})


@login_required
def read_later_list(request):
    """稍后阅读列表"""
    read_laters = ReadLater.objects.filter(
        user=request.user
    ).select_related('article__feed').order_by('-created_at')
    return render(request, 'reader/read_later.html', {'read_laters': read_laters})


@login_required
@require_POST
def add_favorite(request, article_id):
    """添加收藏"""
    article = get_object_or_404(Article, pk=article_id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        article=article
    )
    if created:
        messages.success(request, '已添加到收藏')
    else:
        messages.info(request, '已经在收藏中')
    return redirect('core:article_detail', pk=article_id)


@login_required
@require_POST
def remove_favorite(request, article_id):
    """取消收藏"""
    favorite = get_object_or_404(
        Favorite,
        user=request.user,
        article_id=article_id
    )
    favorite.delete()
    messages.success(request, '已取消收藏')
    return redirect('reader:favorites')


@login_required
@require_POST
def add_read_later(request, article_id):
    """添加到稍后阅读"""
    article = get_object_or_404(Article, pk=article_id)
    read_later, created = ReadLater.objects.get_or_create(
        user=request.user,
        article=article
    )
    if created:
        messages.success(request, '已添加到稍后阅读')
    else:
        messages.info(request, '已经在稍后阅读中')
    return redirect('core:article_detail', pk=article_id)


@login_required
@require_POST
def remove_read_later(request, article_id):
    """从稍后阅读移除"""
    read_later = get_object_or_404(
        ReadLater,
        user=request.user,
        article_id=article_id
    )
    read_later.delete()
    messages.success(request, '已从稍后阅读移除')
    return redirect('reader:read_later')


@login_required
@require_POST
def mark_as_read(request, article_id):
    """标记为已读"""
    article = get_object_or_404(Article, pk=article_id)
    status, created = ReadingStatus.objects.get_or_create(
        user=request.user,
        article=article,
        defaults={'is_read': True}
    )
    if not created and not status.is_read:
        status.is_read = True
        status.save()
    messages.success(request, '已标记为已读')
    return redirect('core:article_detail', pk=article_id)
