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
uv add Django==5.2.6 djangorestframework==3.16.1 python-keycloak==5.8.1

# Create project
django-admin startproject django_drf_keycloak_auth_example .
```
