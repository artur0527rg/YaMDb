from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.validators import ValidationError

from reviews.models import User, Category


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

    email = serializers.EmailField(
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


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор для UserViewSet.'''

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'      
        )


class UserMeSerializer(serializers.ModelSerializer):
    '''Сериализатор для UserViewSet для пользователя.'''

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)


class CategoriesSerializer(serializers.ModelSerializer):
    '''Сериализатор для CategoriesViewSet'''

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url':{'lookup_field':'slug'}
        }
