from django.contrib.auth.models import AbstractUser
from django.db import models

from products.models import Product


class City (models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
    def __str__(self):
        return self.name


class User(AbstractUser):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if self.pk is None and self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return super().username

class FavoriteItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="users_favorite"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="products_favorite"
    )

    class Meta:
        verbose_name = "Избранное пользователя"
        verbose_name_plural = "Избранное пользователей"
        unique_together = ('user', 'product')