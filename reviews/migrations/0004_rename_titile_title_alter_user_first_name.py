# Generated by Django 4.1.5 on 2023-01-24 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_category_genre_titile'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Titile',
            new_name='Title',
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
