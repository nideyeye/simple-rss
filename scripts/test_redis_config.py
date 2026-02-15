#!/usr/bin/env python
"""
Redis 配置测试脚本
测试 Redis 缓存连接和基本功能
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.core.cache import cache


def test_redis_connection():
    """测试 Redis 连接"""
    print("测试 Redis 连接...")

    # 测试写入
    cache.set('test_key', 'test_value', 60)
    print("✓ 写入测试数据成功")

    # 测试读取
    value = cache.get('test_key')
    if value == 'test_value':
        print("✓ 读取测试数据成功")
    else:
        print("✗ 读取测试数据失败")
        return False

    # 测试删除
    cache.delete('test_key')
    if cache.get('test_key') is None:
        print("✓ 删除测试数据成功")
    else:
        print("✗ 删除测试数据失败")
        return False

    # 测试缓存配置
    print(f"\n缓存配置信息:")
    print(f"  - 后端: {cache.__class__.__module__}.{cache.__class__.__name__}")
    print(f"  - 默认超时: {cache.default_timeout} 秒")

    return True


def test_cache_performance():
    """测试缓存性能"""
    import time

    print("\n测试缓存性能...")

    # 测试多次写入
    start_time = time.time()
    for i in range(100):
        cache.set(f'perf_test_{i}', f'value_{i}', 60)
    write_time = time.time() - start_time
    print(f"✓ 100 次写入耗时: {write_time:.3f} 秒")

    # 测试多次读取
    start_time = time.time()
    for i in range(100):
        cache.get(f'perf_test_{i}')
    read_time = time.time() - start_time
    print(f"✓ 100 次读取耗时: {read_time:.3f} 秒")

    # 清理测试数据
    for i in range(100):
        cache.delete(f'perf_test_{i}')


def main():
    """主函数"""
    print("=" * 50)
    print("Redis 配置测试")
    print("=" * 50)

    try:
        if test_redis_connection():
            test_cache_performance()
            print("\n" + "=" * 50)
            print("所有测试通过！Redis 配置正常。")
            print("=" * 50)
            return 0
        else:
            print("\n" + "=" * 50)
            print("测试失败，请检查 Redis 配置。")
            print("=" * 50)
            return 1

    except Exception as e:
        print(f"\n✗ 测试过程中发生错误: {e}")
        print("\n可能的原因:")
        print("  1. Redis 服务未启动")
        print("  2. Redis 连接配置错误")
        print("  3. django-redis 包未安装")
        print("\n解决方案:")
        print("  1. 启动 Redis: brew services start redis")
        print("  2. 检查配置: config/settings/base.py 中的 REDIS_* 配置")
        print("  3. 安装依赖: uv sync --all-extras")
        return 1


if __name__ == '__main__':
    sys.exit(main())
