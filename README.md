# django-drf-keycloak-auth-example-back-end

- [django-drf-keycloak-auth-example-back-end](#django-drf-keycloak-auth-example-back-end)
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
  - [API 文档](#api-文档)
    - [Install drf-spectacular](#install-drf-spectacular)
    - [Update settings](#update-settings-1)
    - [在 urls.py 中加入 schema 与 UI 视图](#在-urlspy-中加入-schema-与-ui-视图)
  - [Others](#others)

## Init project

```bash
# Initialize the project by uv
uv init django-drf-keycloak-auth-example-back-end -p 3.11

# Create a virtual environment
cd django-drf-keycloak-auth-example-back-end
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

## API 文档

在 DRF 中，也可以生成像 Swagger 那样的 API docs。

> DRF 已经移除了 coreapi 包，所以现在已经停止使用 `coreapi/include_docs_urls` 的形式创建 API 文档。
> 
> 而是改用 DRF 的 `OpenAPI AutoSchema` 或者更强大的第三方模块 [drf-spectacular](https://github.com/tfranzel/drf-spectacular) 或者 [drf-yasg](https://github.com/axnsan12/drf-yasg)。
> 
> 另外，[drf-yasg](https://github.com/axnsan12/drf-yasg) 只支持 `OpenAPI 2.0`，如果希望使用 `OpenAPI 3.0` 建议使用 [drf-spectacular](https://github.com/tfranzel/drf-spectacular)。

### Install drf-spectacular

`drf-spectacular` 是一个现代且被广泛使用的 `DRF OpenAPI（OpenAPI 3）` 生成器。它会基于 `DRF Serializer / ViewSet / APIView` 自动生成 `OpenAPI 3 schema`，并提供 `Swagger / ReDoc` 的视图。推荐用于生产环境替代老旧的 `coreapi` 文档方案。

```bash
# Install using uv
uv add drf-spectacular
```

### Update settings

```py
import os
from urllib.parse import urljoin

# add drf-spectacular to installed apps in settings.py
INSTALLED_APPS = [
    # ALL YOUR APPS
    "drf_spectacular",
]

# Register our spectacular AutoSchema with DRF.
REST_FRAMEWORK = {
    # YOUR SETTINGS
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

KEYCLOAK_SERVER_URL = os.environ.get("KEYCLOAK_SERVER_URL")
KEYCLOAK_REALM = os.environ.get("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = os.environ.get("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = os.environ.get("KEYCLOAK_CLIENT_SECRET")

# drf_spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "Django DRF Keycloak example API",
    "DESCRIPTION": "API docs for Django DRF Keycloak",
    "VERSION": "1.0.0",
    # 可选：指定默认 servers
    "SERVERS": [
        {"url": "http://localhost:8005", "description": "Local dev server"},
    ],
    # 把请求模型与响应模型拆开，便于阅读与复用
    "COMPONENT_SPLIT_REQUEST": True,
    # 定义全局默认使用哪个方案
    "SECURITY": [
        {"BearerAuth": []},
        # {"OpenID": ["openid", "profile", "email"]},
        # {"OAuth2": ["openid", "profile", "email"]},
    ],
    # 定义有哪些认证方案
    "SECURITY_SCHEMES": {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        },
        "OpenID": {
            "type": "openIdConnect",
            "openIdConnectUrl": urljoin(
                KEYCLOAK_SERVER_URL.rstrip("/"),
                f"/realms/{KEYCLOAK_REALM}/.well-known/openid-configuration",
            ),
        },
        "OAuth2": {
            "type": "oauth2",
            "flows": {
                "authorizationCode": {
                    "authorizationUrl": urljoin(
                        KEYCLOAK_SERVER_URL.rstrip("/"),
                        f"/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth",
                    ),
                    "tokenUrl": urljoin(
                        KEYCLOAK_SERVER_URL.rstrip("/"),
                        f"/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token",
                    ),
                    "scopes": {
                        "openid": "OpenID connect scope",
                        "profile": "Access user profile",
                        "email": "Access user email",
                    },
                }
            },
        },
    },
}
```

### 在 urls.py 中加入 schema 与 UI 视图

> 最常见的做法是添加三个 endpoint: OpenAPI JSON、Swagger UI、ReDoc。
>
> 浏览器打开:
>
> `/api/schema/`: 返回 OpenAPI JSON（或 YAML，取决于请求）
>
> `/api/schema/swagger-ui/`: 交互式 Swagger UI
>
> `/api/schema/redoc/`: ReDoc 页面

```py
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # OpenAPI schema(JSON/YAML)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI(interactive)
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # ReDoc(漂亮的静态文档)
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
```

## Others

```bash
# Use PyPI by default; only use TestPyPI when specifically required.
uv pip install --no-cache-dir \
  --index-url https://pypi.org/simple \
  --extra-index-url https://test.pypi.org/simple \
  --index-strategy unsafe-best-match \
  django-drf-keycloak-auth==2025.10.21

uv pip install --index-url https://test.pypi.org/simple django-drf-keycloak-auth==2025.10.21

# Uninstall
uv pip uninstall django-drf-keycloak-auth
```
