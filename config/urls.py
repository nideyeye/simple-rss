"""
config/urls.py
主URL配置
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('reader/', include('reader.urls')),
]

# 开发环境提供静态文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # 可选：使用django-debug-toolbar
    # try:
    #     import debug_toolbar
    #     urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    # except ImportError:
    #     pass
