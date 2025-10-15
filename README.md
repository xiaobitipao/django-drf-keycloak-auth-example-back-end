# django-drf-keycloak-auth-example

- [django-drf-keycloak-auth-example](#django-drf-keycloak-auth-example)
  - [Init project](#init-project)
  - [Initial configuration](#initial-configuration)
    - [Update settings.py](#update-settingspy)
    - [Update urls.py](#update-urlspy)
    - [Start](#start)
  - [Resolve CORS](#resolve-cors)
  - [Keycload OAuth](#keycload-oauth)
    - [Append django-drf-keycloak-auth to `sys.path`](#append-django-drf-keycloak-auth-to-syspath)
    - [Install django-drf-keycloak-auth](#install-django-drf-keycloak-auth)
    - [Update settings](#update-settings)
    - [update urls](#update-urls)
    - [Prepare environment about Keycloak](#prepare-environment-about-keycloak)

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

## Initial configuration

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

## Keycload OAuth

### <del>Append django-drf-keycloak-auth to `sys.path`</del>

```bash
uv run python sitecustomize_install.py
```

### Install django-drf-keycloak-auth

```bash
uv add django-drf-keycloak-auth==0.0.1
```

### Update settings

```py
INSTALLED_APPS = [
    ...
    "django_drf_keycloak_auth",
]


# DRF authentication by Keycloak
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "django_drf_keycloak_auth.authentication.KeycloakAuthentication",
    ],
}


TEMPLATES = [
    {
        ...
        "DIRS": [BASE_DIR / "django_drf_keycloak_auth_example" / "templates"],
    },
]
```

### update urls

```py
from django.urls import include
path("", include("django_drf_keycloak_auth.urls")),
```

### Prepare environment about Keycloak

Create a `.env` file with the following content.

```bash
KEYCLOAK_SERVER_URL=http://localhost:8080/
KEYCLOAK_REALM=example_realm
KEYCLOAK_CLIENT_ID=
KEYCLOAK_CLIENT_SECRET=
```
