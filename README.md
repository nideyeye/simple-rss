# Simple RSS

个人自用的极简 RSS 阅读器，由 AI 驱动开发。

## 系统架构

1. 使用 sqlite3 进行数据库存储
2. 使用 Django 作为后端框架
3. 前端页面使用 Jinja2 编写

## 功能描述

1. 支持 RSS 订阅源自动添加
2. 支持 CloudFlare 域名进行 RSS 订阅代理获取订阅源信息
3. 后台定时自动拉取
4. 支持对接翻译接口实现语言翻译
5. 支持稍后阅读/收藏

## 项目结构

```
simple-rss/
├── manage.py                     # Django 管理脚本
├── pyproject.toml                # 项目依赖配置
├── README.md                     # 项目说明
├── CLAUDE.md                     # Claude Code 项目指南
├── .gitignore                    # Git 忽略配置
│
├── config/                       # Django 主项目配置目录
│   ├── __init__.py
│   ├── jinja2.py                 # Jinja2 模板配置
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py              # 基础配置
│   │   ├── development.py       # 开发环境配置
│   │   ├── production.py        # 生产环境配置
│   │   └── local_settings.py    # 本地开发配置（不提交）
│   ├── urls.py                  # 主 URL 配置
│   ├── wsgi.py                  # WSGI 配置
│   └── asgi.py                  # ASGI 配置
│
├── core/                         # 核心 Django 应用
│   ├── __init__.py
│   ├── admin.py                 # 管理后台配置
│   ├── apps.py                  # 应用配置
│   ├── models.py                # 数据模型
│   │   ├── Feed（订阅源）
│   │   ├── Article（文章）
│   │   ├── Category（分类）
│   │   └── UserProfile（用户配置）
│   ├── views.py                 # 视图
│   ├── urls.py                  # 应用 URL 配置
│   ├── forms.py                 # 表单
│   ├── tests/                   # 测试
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   └── test_services.py
│   └── services/                 # 业务逻辑服务
│       ├── __init__.py
│       ├── fetcher.py           # RSS 抓取服务
│       ├── parser.py            # RSS 解析服务
│       └── translator.py        # 翻译服务
│
├── reader/                       # 阅读器功能应用
│   ├── __init__.py
│   ├── admin.py                 # 管理后台配置
│   ├── apps.py                  # 应用配置
│   ├── models.py                # 阅读状态、收藏、稍后阅读
│   ├── views.py                 # 视图
│   ├── urls.py                  # 应用 URL 配置
│   ├── forms.py                 # 表单
│   └── tests/                   # 测试
│       ├── __init__.py
│       ├── test_models.py
│       └── test_views.py
│
├── templates/                    # Jinja2 模板目录
│   ├── base/
│   │   ├── base.html            # 基础模板
│   │   └── nav.html             # 导航栏
│   ├── core/
│   │   ├── feed_list.html       # 订阅源列表
│   │   ├── feed_detail.html     # 订阅源详情
│   │   ├── article_list.html    # 文章列表
│   │   └── article_detail.html  # 文章详情
│   └── reader/
│       ├── favorites.html       # 收藏列表
│       └── read_later.html      # 稍后阅读
│
├── static/                       # 静态文件目录
│   ├── css/
│   │   └── style.css            # 主样式表
│   ├── js/
│   │   └── main.js              # 主脚本
│   └── images/
│
├── media/                        # 用户上传文件
│
├── utils/                        # 工具模块
│   ├── __init__.py
│   ├── cloudflare_proxy.py      # CloudFlare 代理工具
│   ├── feed_parser.py           # Feed 解析工具
│   └── translation_client.py    # 翻译客户端
│
├── scripts/                      # 工具脚本
│   ├── init_db.py               # 数据库初始化脚本
│   └── migrate_data.py          # 数据迁移脚本
│
└── celery_tasks/                 # Celery 定时任务
    ├── __init__.py
    ├── celery.py                # Celery 配置
    └── tasks.py                 # 定时任务定义
```

## 快速开始

### 环境要求

- Python >= 3.10
- uv（推荐）或 pip

### 安装步骤

1. 创建虚拟环境并安装依赖：
```bash
# 使用 uv（推荐）
uv venv
source .venv/bin/activate  # macOS/Linux
uv sync

# 或使用 pip
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

2. 运行数据库迁移：
```bash
python manage.py migrate
```

3. 初始化数据库（可选）：
```bash
python scripts/init_db.py
```

4. 创建超级用户：
```bash
python manage.py createsuperuser
```

5. 启动开发服务器：
```bash
python manage.py runserver
```

6. 访问应用：
- 前端：http://localhost:8000/
- 管理后台：http://localhost:8000/admin/

### 管理命令

```bash
# 创建 Django 应用
python manage.py startapp <app_name>

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 运行测试
python manage.py test

# Django shell
python manage.py shell

# 收集静态文件（生产环境）
python manage.py collectstatic
```

## 配置说明

### CloudFlare 代理

在 `config/settings/local_settings.py` 中配置：

```python
CLOUDFLARE_PROXY_DOMAIN = 'https://your-worker.workers.dev'
```

### 翻译服务

在 `config/settings/local_settings.py` 中配置翻译 API：

```python
TRANSLATION_API_URL = 'https://api.example.com/translate'
TRANSLATION_API_KEY = 'your-api-key'
```

## 定时任务

使用 Celery 实现定时任务：

1. 启动 Celery worker：
```bash
celery -A celery_tasks worker -l info
```

2. 启动 Celery beat（定时调度）：
```bash
celery -A celery_tasks beat -l info
```

## 开发指南

详细的开发指南请参考 [CLAUDE.md](./CLAUDE.md)。

## 许可证

MIT
