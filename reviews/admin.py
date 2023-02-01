from django.contrib import admin

from .models import Genre, Category, Title, User, Review, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)