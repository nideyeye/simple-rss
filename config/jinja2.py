"""
Jinja2 模板环境配置
"""
from jinja2 import Environment
from django.urls import reverse
from django.utils import dateformat
from django.template.context_processors import csrf
from django.middleware.csrf import get_token


def url(name, *args, **kwargs):
    """Jinja2 url 函数"""
    return reverse(name, args=args, kwargs=kwargs)


def csrf_token_input(request=None):
    """生成 CSRF token input"""
    token = get_token(request) if request else ''
    return f'<input type="hidden" name="csrfmiddlewaretoken" value="{token}">'


def date_filter(value, format_str='Y-m-d H:i'):
    """日期格式化过滤器"""
    if not value:
        return ''
    return dateformat.format(value, format_str)


def truncatewords_filter(value, words=30):
    """截断文字过滤器"""
    if not value:
        return ''
    import re
    word_list = re.split(r'\s+', str(value))
    if len(word_list) <= words:
        return value
    return ' '.join(word_list[:words]) + '...'


def environment(**options):
    """配置Jinja2环境"""
    # 启用自动转义
    options.setdefault('autoescape', True)
    env = Environment(**options)

    # 添加自定义全局函数
    env.globals['url'] = url

    # 添加自定义过滤器
    env.filters['date'] = date_filter
    env.filters['truncatewords'] = truncatewords_filter

    return env
