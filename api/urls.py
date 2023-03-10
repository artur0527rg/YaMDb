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
    CommentViewSet,
    ReviewsViewSet,
    TitlesViewSet,
    CategoriesViewSet,
    GenresViewSet,
    UserViewSet,
    get_confirmation_message,
    get_token
)

v1_router = DefaultRouter()

v1_router.register(
    'categories',
    CategoriesViewSet,
    basename='categories'
)

v1_router.register(
    'genres',
    GenresViewSet,
    basename="genres"
)

v1_router.register(
    'titles',
    TitlesViewSet,
    basename='titles'
)

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

v1_router.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/email/', get_confirmation_message),
    path('auth/token/', get_token)
]
