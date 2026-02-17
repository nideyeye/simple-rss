"""
文章处理工具函数
"""
import logging
import hashlib
from core.models import Article

logger = logging.getLogger(__name__)


def generate_content_hash(title, summary, content):
    """生成文章内容的哈希值，用于检测内容变化"""
    content_str = f"{title}|{summary}|{content}"
    return hashlib.md5(content_str.encode('utf-8')).hexdigest()


def save_or_update_article(feed, entry):
    """
    保存或更新文章
    如果文章不存在则创建，如果存在但内容不同则更新

    Args:
        feed: Feed 订阅源对象
        entry: 解析后的文章条目字典

    Returns:
        tuple: (is_new, article) - is_new表示是否是新文章或更新的文章
    """
    # 获取唯一标识符和实际链接
    guid = entry.get('guid', entry['link'])
    link = entry['link']

    title = entry['title'] or '无标题'
    summary = entry.get('summary', '')
    content = entry.get('content', '')

    # 使用 filter().first() 查询文章
    # 优先使用 guid 查询，如果 guid 和 link 不同且未找到，再尝试用 link 查询
    article = Article.objects.filter(feed=feed, url=guid).first()
    if not article and guid != link:
        article = Article.objects.filter(feed=feed, url=link).first()

    if article:
        # 检查内容是否有变化
        if (article.title != title or
            article.summary != summary or
            article.content != content):

            # 内容有变化，更新文章
            article.title = title
            article.author = entry.get('author', '')
            article.summary = summary
            article.content = content
            article.pub_date = entry.get('pub_date')
            article.save()
            logger.info(f"更新文章: {title}")
            return (True, article)

        # 内容没有变化
        return (False, article)
    else:
        # 文章不存在，创建新文章
        # 使用实际的链接作为 url，确保用户可以点击访问
        article = Article.objects.create(
            feed=feed,
            title=title,
            url=link,
            author=entry.get('author', ''),
            summary=summary,
            content=content,
            pub_date=entry.get('pub_date'),
        )
        logger.info(f"创建新文章: {title}")
        return (True, article)
