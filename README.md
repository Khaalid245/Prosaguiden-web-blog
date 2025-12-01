# Prosaguiden Web Blog — Backend

## Overview

This is the backend of the Prosaguiden web blog system, built with **Django + Django REST Framework (DRF)** using **MySQL**. Authentication uses **JWT tokens** via **DRF SimpleJWT**.

## ✅ Step 1 — Backend Initialization

### Completed Tasks:

1. Created `backend/` folder with virtual environment `.venv`.
2. Installed dependencies:

```
pip install django djangorestframework mysqlclient Pillow
pip install djangorestframework-simplejwt
```

3. Created Django project: `config`
4. Created apps:

   - `users`
   - `articles`
   - `comments`
   - `feedback`

5. Added apps + REST framework + JWT to `INSTALLED_APPS`.
6. Configured MySQL in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blogdb',
        'USER': 'bloguser',
        'PASSWORD': 'securepassword',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

7. Configured MEDIA storage:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

8. Configured JWT authentication:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```

## ✅ Step 2 — User Authentication & Roles

### Completed Tasks:

1. Created **custom User model** with roles (Admin, Writer, Reader) in `users/models.py`.
2. Configured Django to use it:

```python
AUTH_USER_MODEL = 'users.User'
```

3. Created **serializers** for registration in `users/serializers.py`.
4. Created **views** for registration in `users/views.py`.
5. Created **URLs** in `users/urls.py`:

```
POST /api/auth/register/  → Register new user
POST /api/auth/login/     → Obtain JWT tokens
POST /api/auth/refresh/   → Refresh JWT tokens
```

6. Ran migrations:

```
python manage.py makemigrations
python manage.py migrate
```

7. Tested endpoints successfully:

   - Registration works
   - Login returns access + refresh tokens
   - User roles exist

## ✅ Current Status

- Backend running on `http://localhost:8000`
- JWT authentication functional
- User registration & login operational
- Database connected and migrations applied

## Next Steps

- Create Article and Category models
- Build CRUD endpoints for articles and comments
- Implement permissions based on user roles
- Connect frontend with backend APIs
