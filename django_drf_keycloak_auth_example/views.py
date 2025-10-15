from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


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
