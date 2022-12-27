from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.validators import ValidationError

from reviews.models import User

class SignUpSerializer(serializers.Serializer):
    password = None
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )

class TokenSerializer(serializers.Serializer):
    """Сериализатор для метода get_token."""

    username = serializers.CharField(
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )

    def validate_confirmation_code(self, value):
        if value == '':
            raise ValidationError('Это поле не может быть пустым.')
        return value