from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.validators import ValidationError

from reviews.models import User, Category, Genre, Title, Review, Comment


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


class GenresSerializer(serializers.ModelSerializer):
    '''Сериализатор для GenresViewSet'''

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field':'slug'}
        }

class ReadTitleSerializer(serializers.ModelSerializer):
    '''Сериализатор для TitlesViewSet на чтение'''

    genre = GenresSerializer(read_only=True, many=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )


class WriteTitleSerializer(serializers.ModelSerializer):
    '''Сериализатор для TitlesViewSet на запись'''
    
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset = Genre.objects.all(),
        many = True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset = Category.objects.all(),
        required = False
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category'
        )

        def validate_year(self, value):
            '''Проверка поля year на адекватность значений'''

            if value > timezone.now().year:
                raise serializers.ValidationError(
                    'Год выпуска не может быть больше настоящего'
                )
            return value


class ReviewSerializer(serializers.ModelSerializer):
    '''Сериализатор для ReviewViewSet'''

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only = True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST' 
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Можно оставить только один отзыв на произведение!')
        return data


    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор для CommentViewSet'''
    
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only = True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment