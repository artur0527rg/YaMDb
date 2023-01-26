from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from api.filters import TitleFilter
from api.mixins import CreateListDestroyViewSet
from api.permissions import AdminOrReadOnly, IsAdmin, IsAuthorOrStaffOrReadOnly
from api.serializers import (
    ReviewSerializer,
    WriteTitleSerializer,
    ReadTitleSerializer,
    GenresSerializer,
    SignUpSerializer,
    TokenSerializer,
    UserSerializer,
    UserMeSerializer,
    CategoriesSerializer
)
from reviews.models import User, Category, Genre, Title

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmation_message(request):
    '''Отправка кода подтверждения на email пользователя(регистрация).'''

    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user, _ = User.objects.get_or_create(
            username = serializer.validated_data['username'],
            email = serializer.validated_data['email']
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения',
            f'Ваш код: {confirmation_code}',
            DEFAULT_FROM_EMAIL,
            [serializer.validated_data['email']]
        )
        return Response({
            'email': serializer.validated_data['email'],
            'username': serializer.validated_data['username']},
            status=status.HTTP_200_OK
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    '''Получения токена для запросов.'''

    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, email=serializer.validated_data['email'])
        if default_token_generator.check_token(
            user,
            serializer.validated_data['confirmation_code']
        ):
            token = AccessToken.for_user(user)
            return Response({'token':str(token)}, status=status.HTTP_201_CREATED)
        return Response({'error':'invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserViewSet(viewsets.ModelViewSet):
    '''Вьюсет для users.'''

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=UserMeSerializer 
    )
    def me(self, request):
        self.kwargs['username'] = request.user.username
        if self.request.method == "PATCH":
            self.partial_update(request)
            request.user.refresh_from_db()
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class CategoriesViewSet(CreateListDestroyViewSet):
    '''Вьюсет для category.'''

    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(CreateListDestroyViewSet):
    '''Вьюсет для genres.'''

    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    '''Вьюсет для titles.'''
 
    queryset = Title.objects.annotate(
        rating = Avg('reviews__score')
    ).all()
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadTitleSerializer
        return WriteTitleSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    '''Вьюсет для reviews.'''

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly,)

    def get_queryset(self, *args, **kwargs):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)