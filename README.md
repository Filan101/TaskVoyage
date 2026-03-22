# TaskVoyage 项目详细文档

## 项目概述

TaskVoyage 是一个基于 Django 和 React 的任务管理系统，用于帮助用户管理个人任务，支持任务的创建、编辑、删除、状态管理等功能。

## 项目结构

```
TaskVoyage/
├── backend/                  # 后端 Django 项目
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py           # 项目配置文件
│   ├── urls.py               # URL 路由配置
│   └── wsgi.py
├── frontend/                 # 前端静态文件
│   ├── css/                  # CSS 样式文件
│   │   └── style.css
│   ├── images/               # 图片资源
│   │   ├── good.svg
│   │   ├── lose.svg
│   │   └── proceed.svg
│   ├── js/                   # JavaScript 文件
│   │   ├── api.js
│   │   ├── app.js
│   │   └── login.js
│   ├── index.html            # 主页面
│   └── login.html            # 登录页面
├── tasks/                    # 任务管理应用
│   ├── migrations/           # 数据库迁移文件
│   │   ├── 0001_initial.py
│   │   ├── 0002_task_user.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py              # 后台管理配置
│   ├── apps.py               # 应用配置
│   ├── models.py             # 任务模型
│   ├── serializers.py        # 任务序列化器
│   ├── urls.py               # 任务相关路由
│   └── views.py              # 任务相关视图
├── users/                    # 用户管理应用
│   ├── migrations/           # 数据库迁移文件
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py              # 后台管理配置
│   ├── apps.py               # 应用配置
│   ├── models.py             # 用户模型
│   ├── serializers.py        # 用户序列化器
│   ├── urls.py               # 用户相关路由
│   └── views.py              # 用户相关视图
├── 启动/                     # 启动脚本
│   ├── start_project.bat
│   └── start_project.py
├── manage.py                 # Django 管理脚本
└── requirements.txt          # 项目依赖
```

## 技术栈

### 后端
- **Django 3.2+**：Python Web 框架
- **Django REST Framework**：RESTful API 开发
- **django-cors-headers**：跨域请求支持
- **djangorestframework-simplejwt**：JWT 认证
- **PyMySQL**：MySQL 数据库驱动
- **Pillow**：图像处理
- **PyJWT**：JWT 令牌处理

### 前端
- **HTML5/CSS3**：页面结构和样式
- **JavaScript (ES6+)**：前端交互逻辑
- **原生 AJAX**：API 调用

## 核心功能

### 1. 用户管理
- **用户注册**：支持手机号和用户名注册
- **用户登录**：基于 JWT 的身份验证
- **个人资料**：查看和管理个人信息

### 2. 任务管理
- **任务创建**：创建新任务，支持标题、描述、截止日期、图片等
- **任务列表**：查看所有任务，支持按状态筛选和排序
- **任务详情**：查看任务详细信息
- **任务编辑**：修改任务信息
- **任务删除**：删除不需要的任务
- **任务状态更新**：标记任务为已完成或待完成

### 3. 统计功能
- **任务统计**：总任务数、已完成任务数、待完成任务数、逾期任务数
- **完成率**：任务完成率统计
- **即将到期任务**：显示即将到期的任务

## 数据库设计

### 用户表 (users)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| id | BigAutoField | 主键 | 用户ID |
| username | CharField(50) | 唯一 | 用户名 |
| phone | CharField(11) | 唯一 | 手机号 |
| email | EmailField | 可空 | 邮箱 |
| avatar | URLField | 可空 | 头像URL |
| password | CharField | - | 密码（哈希存储） |
| created_at | DateTimeField | 默认当前时间 | 创建时间 |
| updated_at | DateTimeField | 自动更新 | 更新时间 |
| is_active | BooleanField | 默认True | 是否激活 |
| is_staff | BooleanField | 默认False | 是否为管理员 |
| is_superuser | BooleanField | 默认False | 是否为超级用户 |

### 任务表 (tasks)
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| id | BigAutoField | 主键 | 任务ID |
| user_id | ForeignKey | 外键关联users表 | 用户ID |
| title | CharField(200) | - | 任务标题 |
| description | TextField | 可空 | 任务描述 |
| image | URLField | 可空 | 任务图片URL |
| status | CharField(20) | 默认'pending' | 任务状态（pending/completed） |
| created_at | DateTimeField | 默认当前时间 | 创建时间 |
| deadline | DateTimeField | - | 截止日期 |
| completed_at | DateTimeField | 可空 | 完成时间 |
| updated_at | DateTimeField | 自动更新 | 更新时间 |

## API 接口

### 用户相关接口

#### 1. 注册接口
- **URL**：`/api/users/register/`
- **方法**：POST
- **请求体**：
  ```json
  {
    "phone": "13800138000",
    "username": "testuser",
    "password": "password123"
  }
  ```
- **响应**：
  ```json
  {
    "message": "注册成功",
    "user": {
      "id": 1,
      "username": "testuser",
      "phone": "13800138000",
      "email": null,
      "avatar": null
    }
  }
  ```

#### 2. 登录接口
- **URL**：`/api/users/login/`
- **方法**：POST
- **请求体**：
  ```json
  {
    "phone": "13800138000",
    "password": "password123"
  }
  ```
- **响应**：
  ```json
  {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

#### 3. 获取个人资料
- **URL**：`/api/users/profile/`
- **方法**：GET
- **请求头**：`Authorization: Bearer <access_token>`
- **响应**：
  ```json
  {
    "id": 1,
    "username": "testuser",
    "phone": "13800138000",
    "email": null,
    "avatar": null
  }
  ```

### 任务相关接口

#### 1. 获取任务列表
- **URL**：`/api/tasks/`
- **方法**：GET
- **请求头**：`Authorization: Bearer <access_token>`
- **查询参数**：
  - `status`：筛选任务状态（pending/completed）
  - `sort`：排序方式（name/createdAt/status）
- **响应**：
  ```json
  [
    {
      "id": 1,
      "title": "完成项目文档",
      "description": "编写项目详细文档",
      "image": null,
      "status": "pending",
      "created_at": "2026-03-06T10:00:00Z",
      "deadline": "2026-03-10T18:00:00Z",
      "completed_at": null
    }
  ]
  ```

#### 2. 创建任务
- **URL**：`/api/tasks/`
- **方法**：POST
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体**：
  ```json
  {
    "title": "完成项目文档",
    "description": "编写项目详细文档",
    "deadline": "2026-03-10T18:00:00Z",
    "image": "https://example.com/image.jpg"
  }
  ```
- **响应**：
  ```json
  {
    "message": "任务创建成功",
    "task": {
      "id": 1,
      "title": "完成项目文档",
      "description": "编写项目详细文档",
      "image": "https://example.com/image.jpg",
      "status": "pending",
      "created_at": "2026-03-06T10:00:00Z",
      "deadline": "2026-03-10T18:00:00Z",
      "completed_at": null
    }
  }
  ```

#### 3. 更新任务
- **URL**：`/api/tasks/<task_id>/`
- **方法**：PUT
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体**：
  ```json
  {
    "title": "完成项目文档（更新）",
    "status": "completed"
  }
  ```
- **响应**：
  ```json
  {
    "message": "任务更新成功",
    "task": {
      "id": 1,
      "title": "完成项目文档（更新）",
      "description": "编写项目详细文档",
      "image": "https://example.com/image.jpg",
      "status": "completed",
      "created_at": "2026-03-06T10:00:00Z",
      "deadline": "2026-03-10T18:00:00Z",
      "completed_at": "2026-03-06T12:00:00Z"
    }
  }
  ```

#### 4. 删除任务
- **URL**：`/api/tasks/<task_id>/`
- **方法**：DELETE
- **请求头**：`Authorization: Bearer <access_token>`
- **响应**：
  ```json
  {
    "message": "任务删除成功"
  }
  ```

#### 5. 获取任务统计
- **URL**：`/api/tasks/stats/`
- **方法**：GET
- **请求头**：`Authorization: Bearer <access_token>`
- **响应**：
  ```json
  {
    "total": 5,
    "completed": 2,
    "pending": 3,
    "overdue": 1,
    "completion_rate": 40.0,
    "upcoming": [
      {
        "id": 2,
        "title": "准备会议材料",
        "deadline": "2026-03-07T10:00:00Z"
      }
    ]
  }
  ```

## 项目配置

### 数据库配置
在 `backend/settings.py` 文件中配置数据库连接：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'do_manager',
        'USER': 'root',
        'PASSWORD': '123456789',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}
```

### JWT 配置
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
```

### 跨域配置
```python
CORS_ALLOW_ALL_ORIGINS = True
```

## 项目启动

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 创建超级用户
```bash
python manage.py createsuperuser
```

### 4. 启动开发服务器
```bash
python manage.py runserver
```

或者使用启动脚本：
```bash
# 在 启动 目录下执行
start_project.bat
```

## 项目特点

1. **前后端分离**：后端提供 RESTful API，前端通过 AJAX 调用
2. **JWT 认证**：使用 JWT 进行身份验证，提高安全性
3. **响应式设计**：前端页面适配不同设备
4. **任务管理**：完整的任务生命周期管理
5. **统计分析**：提供任务完成率和逾期任务统计
6. **安全可靠**：密码哈希存储，权限控制

## 注意事项

1. **数据库配置**：确保 MySQL 数据库已创建，并且配置正确
2. **JWT 密钥**：在生产环境中，应修改 `SECRET_KEY` 为安全的随机字符串
3. **CORS 配置**：在生产环境中，应限制允许的源，而不是使用 `CORS_ALLOW_ALL_ORIGINS = True`
4. **密码安全**：使用强密码，避免使用默认密码
5. **数据备份**：定期备份数据库，防止数据丢失

## 未来扩展

1. **添加任务分类**：支持任务按分类管理
2. **添加任务标签**：支持给任务添加标签
3. **添加任务提醒**：支持任务到期提醒
4. **添加团队协作**：支持多用户协作管理任务
5. **添加数据分析**：提供更详细的任务完成情况分析
6. **优化前端界面**：使用现代前端框架（如 React、Vue）重构前端

## 总结

TaskVoyage 是一个功能完整的任务管理系统，提供了用户管理、任务管理和统计分析等核心功能。项目采用 Django 作为后端框架，提供 RESTful API，前端使用原生 HTML/CSS/JavaScript 实现。系统设计合理，代码结构清晰，易于维护和扩展。
