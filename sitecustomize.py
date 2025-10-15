import os
import sys

# Set the project root directory
# project_root_dir = f'{os.environ["HOME"]}/0/Project/20991231_Z_Private/public/ibm-sso/'
#
# .venv/lib/python3.11/site-packages
example_root = os.path.dirname(os.path.abspath(__file__))

# Get the django_drf_keycloak_auth_module_dir module directory
django_drf_keycloak_auth_module_dir = os.path.join(
    example_root, "../../../../..", "django-drf-keycloak-auth"
)

# Add the django_drf_keycloak_auth_module_dir module directory to sys.path
sys.path.append(django_drf_keycloak_auth_module_dir)
