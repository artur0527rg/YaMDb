from django.contrib import admin

from .models import Genre, Category, Title, User

# Register your models here.
admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)