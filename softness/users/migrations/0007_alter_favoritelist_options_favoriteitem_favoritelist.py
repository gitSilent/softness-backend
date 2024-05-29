# Generated by Django 5.0.6 on 2024-05-29 18:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_favoriteitem_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favoritelist',
            options={'verbose_name': 'Список избранного у пользователя', 'verbose_name_plural': 'Списки избранного у пользователя'},
        ),
        migrations.AddField(
            model_name='favoriteitem',
            name='favoritelist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favoritelist_items', to='users.favoritelist'),
        ),
    ]