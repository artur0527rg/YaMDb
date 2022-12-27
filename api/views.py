from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from .serializers import SignUpSerializer
from reviews.models import User

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmation_message(request):
    '''Отправка кода подтверждения на email пользователя(регистрация)'''

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

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def get_token(request):
#     '''Генерация пользовательского токена'''

    


