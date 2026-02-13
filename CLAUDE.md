# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个个人自用的极简 RSS 阅读器，由 AI 驱动开发。

### 技术栈
- **后端框架**: Django 5.1+
- **数据库**: SQLite3
- **模板引擎**: Jinja2
- **RSS 解析**: feedparser
- **HTTP 请求**: requests
- **定时任务**: Celery + Redis（可选）
- **包管理器**: uv

### 核心功能
1. **RSS 订阅管理** - 支持自动添加 RSS 订阅源
2. **CloudFlare 代理** - 使用 CloudFlare 域名进行 RSS 订阅代理获取订阅源信息
3. **定时任务** - 后台定时自动拉取 RSS 更新（使用 Celery）
4. **翻译功能** - 支持对接翻译接口实现内容语言翻译
5. **阅读管理** - 支持稍后阅读和收藏功能

## 项目结构

项目采用多应用架构，详细结构请参考 README.md。主要目录：

- `config/` - Django 主项目配置（settings 分环境管理）
- `core/` - 核心 Django 应用（Feed、Article、Category 等模型）
- `reader/` - 阅读器功能应用（收藏、稍后阅读）
- `templates/` - Jinja2 模板目录
- `static/` - 静态文件
- `utils/` - 工具模块（CloudFlare 代理、翻译客户端等）
- `celery_tasks/` - Celery 定时任务

## 开发命令

### 环境初始化
```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux

# 同步依赖
uv sync                    # 安装核心依赖
uv sync --all-extras       # 安装所有依赖（包括 Celery）

# 添加新依赖
uv add <package_name>

# 添加开发依赖
uv add --dev <package_name>
```

### Django 管理
```bash
# 运行开发服务器
python manage.py runserver

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# Django shell
python manage.py shell

# 收集静态文件（生产环境）
python manage.py collectstatic
```

### 测试
```bash
# 运行所有测试
python manage.py test

# 运行单个应用的测试
python manage.py test core
python manage.py test reader

# 使用 pytest（推荐）
pytest
pytest core/tests/
pytest -v  # 详细输出

# 运行单个测试文件
pytest core/tests/test_models.py
pytest core/tests/test_views.py::test_article_list
```

### 代码规范
```bash
# 使用 ruff 检查代码
ruff check .

# 自动修复
ruff check --fix .

# 格式化代码
ruff format .
```

### Celery 任务（可选）
```bash
# 启动 Celery worker
celery -A celery_tasks worker -l info

# 启动 Celery beat（定时调度）
celery -A celery_tasks beat -l info
```

## 配置管理

### Settings 分层结构
- `config/settings/base.py` - 基础配置（所有环境共享）
- `config/settings/development.py` - 开发环境配置
- `config/settings/production.py` - 生产环境配置
- `config/settings/local_settings.py` - 本地配置（不提交，用于敏感信息）

### 环境变量
敏感配置应放在 `local_settings.py` 中，该文件已在 `.gitignore` 中排除：

```python
# config/settings/local_settings.py
DEBUG = True

# CloudFlare 代理配置
CLOUDFLARE_PROXY_DOMAIN = 'https://your-worker.workers.dev'

# 翻译服务配置
TRANSLATION_API_URL = 'https://api.example.com/translate'
TRANSLATION_API_KEY = 'your-api-key'

# Celery 配置（如果使用）
CELERY_BROKER_URL = 'redis://localhost:6379/0'
```

## 模板系统

使用 Jinja2 作为模板引擎，配置文件位于 `config/jinja2.py`。

模板文件放在 `templates/` 目录下，按应用分类：
- `templates/base/` - 基础模板和通用组件
- `templates/core/` - core 应用的模板
- `templates/reader/` - reader 应用的模板

## 业务逻辑分层

项目采用服务层模式，将业务逻辑从视图和模型中分离：

- **models.py** - 数据模型定义
- **views.py** - HTTP 请求处理
- **services/** - 业务逻辑服务
  - `fetcher.py` - RSS 抓取服务
  - `parser.py` - RSS 解析服务
  - `translator.py` - 翻译服务
- **utils/** - 通用工具函数
  - `cloudflare_proxy.py` - CloudFlare 代理
  - `translation_client.py` - 翻译客户端

## 开发注意事项

1. **数据库**: SQLite3 数据库文件 `db.sqlite3` 已在 `.gitignore` 中排除
2. **敏感信息**: 所有敏感配置必须通过 `local_settings.py` 管理，不要提交到版本控制
3. **测试**: 新功能必须添加相应的测试（放在各应用的 `tests/` 目录下）
4. **代码规范**: 使用 ruff 进行代码检查和格式化（配置在 `pyproject.toml`）
5. **依赖管理**: 使用 uv 管理依赖，不要手动修改 `requirements.txt`
