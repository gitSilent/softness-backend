from django.db import models
from django.db.models import CheckConstraint, Q

from products.models import Product
from users.models import User


# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user_cart"
    )

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'

    @property
    def total(self):
        return sum([item.amount * item.product.price for item in self.items.all()])

    @property
    def items(self):
        return self.cart_items.all()

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

class CartItem(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="cart_products",
        on_delete=models.CASCADE
    )
    cart = models.ForeignKey(
        Cart,
        related_name="cart_items",
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(default=1)

    @property
    def total(self):
        return self.product.price * self.amount

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
        constraints = [
            CheckConstraint(check=Q(amount__gte=1), name="amount_more_than_0"),
        ]
