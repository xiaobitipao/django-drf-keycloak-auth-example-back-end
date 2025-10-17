from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_drf_keycloak_auth.models.user import User
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView, Request, Response

from django_drf_keycloak_auth_example.permissions import isEmployeeRole


def example_home(request: HttpRequest):
    return render(
        request,
        "home.html",
        {
            "user": request.user,
        },
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def example_get_hello(request):
    return JsonResponse({"message": "Hello from Django + DRF!"})


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def example_post_echo(request):
    data = request.data if hasattr(request, "data") else {}
    return JsonResponse({"received": data, "note": "This is echoed by server."})


class AuthTestPublicView(APIView):

    # No authentication required
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]

    @extend_schema(
        auth=[],
        description="A guest view that does not require authentication.",
    )
    def get(self, request: Request):

        user = request.user

        return Response(
            {
                "ok": True,
                "user": {
                    "username": getattr(user, "username"),
                    "is_active": getattr(user, "is_active"),
                    "is_anonymous": getattr(user, "is_anonymous"),
                    "is_authenticated": getattr(user, "is_authenticated"),
                    "is_staff": getattr(user, "is_staff"),
                    "is_superuser": getattr(user, "is_superuser"),
                },
                "auth": request.auth,
                "roles": getattr(request.user, "roles", []),
            },
            status=status.HTTP_200_OK,
        )


class AuthTestProtectedView(APIView):

    # No authentication required
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer]

    @extend_schema(
        description="An authenticated view that requires authentication.",
    )
    def get(self, request: Request):

        user: User = request.user

        return Response(
            {
                "ok": True,
                "user": user.to_dict(),
                "auth": request.auth,
                "roles": getattr(request.user, "roles", []),
            },
            status=status.HTTP_200_OK,
        )


class AuthTestEmployeeRoleView(APIView):

    # No authentication required
    permission_classes = [isEmployeeRole]
    renderer_classes = [JSONRenderer]

    @extend_schema(
        description="An employee role view that requires the 'employee' role.",
    )
    def get(self, request: Request):

        user: User = request.user

        return Response(
            {
                "ok": True,
                "user": user.to_dict(),
                "auth": request.auth,
                "roles": getattr(request.user, "roles", []),
            },
            status=status.HTTP_200_OK,
        )
