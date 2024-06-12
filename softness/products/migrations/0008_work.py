# Generated by Django 5.0.6 on 2024-06-12 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_old_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='products/works', verbose_name='Фото работы')),
            ],
            options={
                'verbose_name': 'Фото работы',
                'verbose_name_plural': 'Фото работ',
            },
        ),
    ]
