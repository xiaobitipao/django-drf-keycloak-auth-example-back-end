import os

from django_drf_keycloak_auth.models.user import User
from rest_framework import permissions
from rest_framework.request import Request

KEYCLOAK_CLIENT_ID = os.environ.get("KEYCLOAK_CLIENT_ID")


class isEmployeeRole(permissions.BasePermission):
    def has_permission(self, request: Request, view):
        user: User = request.user
        if not user:
            return False
        return user.has_role(KEYCLOAK_CLIENT_ID + ":employee")
