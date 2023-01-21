"""YaMDb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    get_confirmation_message,
    get_token
)

v1_router = DefaultRouter()

v1_router.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/email/', get_confirmation_message),
    path('auth/token/', get_token)
    # /categories/
    # /genres/
    # /titles/
]
