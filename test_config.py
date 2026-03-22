import os
import sys

# 设置 Django 设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

try:
    # 导入 Django
    import django
    django.setup()
    # 导入 settings
    from django.conf import settings
    # 打印数据库配置
    print("Database configuration:")
    print(settings.DATABASES)
    # 验证 dj_database_url 是否被正确导入
    import dj_database_url
    print("\ndj_database_url imported successfully!")
    print("Test completed successfully!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
