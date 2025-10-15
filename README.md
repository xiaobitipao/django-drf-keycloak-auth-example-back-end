# django-drf-keycloak-auth-example

## Init project

```bash
# Initialize the project by uv
uv init django-drf-keycloak-auth-example -p 3.11

# Create a virtual environment
cd django-drf-keycloak-auth-example
uv venv -p 3.11

# Activate the virtual environment
source .venv/bin/activate

# Add dependency
uv add Django==5.2.6 djangorestframework==3.16.1 python-dotenv==1.1.1 python-keycloak==5.8.1

# Create project
django-admin startproject django_drf_keycloak_auth_example .
```

## Initial configuratio

### Update settings.py

```py
INSTALLED_APPS = [
    ...
    "rest_framework",
]
```

### Update urls.py

```py
from . import views
path("example/home/", views.example_home, name="home"),
path("example/hello/", views.example_get_hello, name="hello_get"),
path("example/echo/", views.example_post_echo, name="echo_post"),
```

### Start

```bash
uv run manage.py makemigrations
uv run manage.py migrate

uv run manage.py runserver 8005
```

## Resolve CORS

Install `django-cors-headers` by `uv add django-cors-headers==4.9.0`, and update settings.py.

```py
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INSTALLED_APPS = [
    ...
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware", # Add it at the very beginning, before CommonMiddleware.
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```