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

class FavoriteList(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user_favoritelist"
    )

    def __str__(self):
        return f'Избранное пользователя {self.user.username}'

    @property
    def items(self):
        return self.favoritelist_items.all()

    class Meta:
        verbose_name = "Список избранного у пользователя"
        verbose_name_plural = "Списки избранного у пользователя"
        # unique_together = ('favoritelist', 'product')

class FavoriteItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="products_favorite"
    )
    favoritelist = models.ForeignKey(
        FavoriteList,
        on_delete=models.CASCADE,
        related_name="favoritelist_items",
        null=True
    )

    def user_username(self):
        return self.favoritelist.user.username
    def __str__(self):
        return f'Товар в избранном "{self.product.title}"'

    class Meta:
        verbose_name = "Товар в избранном пользователя"
        verbose_name_plural = "Товары в избранном пользователя"
        unique_together = ('favoritelist', 'product')

