# 订阅源抓取问题排查指南

## 常见问题

### 1. 订阅源创建后没有文章

#### 原因分析

1. **网络超时**：订阅源服务器响应慢或无法访问
   - `https://feeds.feedburner.com/ruanyifeng` 在国内网络环境下可能超时

2. **URL 错误**：订阅源地址不正确或已失效

3. **解析失败**：RSS 格式不符合标准

#### 排查步骤

**步骤 1：查看订阅源状态**
```bash
python manage.py shell -c "
from core.models import Feed
feed = Feed.objects.get(pk=<订阅源ID>)
print(f'标题: {feed.title}')
print(f'URL: {feed.url}')
print(f'最后抓取时间: {feed.last_fetch_at}')
print(f'最后抓取状态: {feed.last_fetch_status}')
"
```

**步骤 2：手动测试抓取**
```bash
# 使用管理命令手动抓取
python manage.py fetch_feed <订阅源ID> --timeout 15

# 示例：抓取 ID 为 2 的订阅源
python manage.py fetch_feed 2 --timeout 15
```

**步骤 3：检查日志**
查看控制台输出，确认具体的错误信息：
- `抓取超时`：网络问题或服务器响应慢
- `抓取失败`：URL 可能不正确
- `解析失败`：RSS 格式问题

### 2. 推荐的测试订阅源

以下订阅源经过测试，可以正常访问：

#### 技术类

- **Django 官方博客**
  - URL: `https://www.djangoproject.com/rss/weblog/`
  - 描述: Django 框架官方博客
  - 更新频率: 每周 1-2 篇

- **Python Planet**
  - URL: `https://planet.python.org/rss20.xml`
  - 描述: Python 社区聚合
  - 更新频率: 每天多篇

#### 新闻类

- **BBC 中文网**
  - URL: `https://www.bbc.com/zhongwen/simp/index.xml`
  - 描述: BBC 中文新闻
  - 更新频率: 每天

- **36Kr**
  - URL: `https://36kr.com/feed`
  - 描述: 科技创业媒体
  - 更新频率: 每天

### 3. 手动抓取命令

创建订阅源后，如果自动抓取失败，可以使用管理命令手动重试：

```bash
# 基本用法
python manage.py fetch_feed <订阅源ID>

# 自定义超时时间（秒）
python manage.py fetch_feed <订阅源ID> --timeout 30

# 示例
python manage.py fetch_feed 1 --timeout 15
```

### 4. 批量抓取所有订阅源

```bash
python manage.py shell -c "
from core.models import Feed
from django.utils import timezone

for feed in Feed.objects.filter(is_active=True):
    print(f'抓取订阅源: {feed.title} (ID: {feed.pk})')
    feed.last_fetch_at = timezone.now()
    feed.save()
"
```

然后逐个使用 `fetch_feed` 命令抓取：

```bash
for feed_id in 1 2 3; do
    echo "抓取订阅源 ID: $feed_id"
    python manage.py fetch_feed $feed_id --timeout 15
done
```

## 网络问题解决方案

### 使用 CloudFlare 代理

如果某些订阅源无法访问，可以配置 CloudFlare Workers 代理：

1. 创建 CloudFlare Worker
2. 配置代理域名
3. 在 `config/settings/local_settings.py` 中配置：

```python
CLOUDFLARE_PROXY_DOMAIN = 'https://your-worker.workers.dev'
```

### 增加 SSL 验证跳过（仅用于测试）

如果遇到 SSL 证书问题，可以修改 `core/services/fetcher.py`：

```python
response = self.session.get(url, timeout=timeout, verify=False)
```

⚠️ **警告**：此方法仅用于测试，生产环境请勿使用。

## 创建订阅源建议

1. **测试 URL**：创建前先用浏览器或命令行测试 URL 是否可访问
   ```bash
   curl -I <RSS_URL>
   ```

2. **使用标准格式**：优先选择支持 RSS 2.0 标准的订阅源

3. **设置合理超时**：如果订阅源服务器响应慢，可以增加超时时间
   - 默认：10 秒
   - 可调整：15-30 秒

4. **检查网络环境**：某些国外订阅源可能需要科学上网

## 联系支持

如果以上方法都无法解决问题，请提供以下信息：

1. 订阅源 URL
2. 错误信息（最后抓取状态）
3. 网络环境（是否使用代理）
