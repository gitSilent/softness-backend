from django.db import models
from django.db.models import QuerySet, CheckConstraint, Q
from rest_framework.exceptions import ValidationError

from products.models import Product
from users.models import User


# Create your models here.
class Order (models.Model):
    class Status(models.TextChoices):
        NEW = ("NW", "Новый")
        IN = ("IN", "В обработке")
        READY = ("RD", "Готов")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_orders"
    )

    info = models.CharField(
        max_length=500,
        verbose_name='Информация о заказе',
        default='Здесь будет информация о заказе'
    )

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        verbose_name='Статус заказа',
        default='NW')

    @property
    def total(self) -> int:
        return sum([item.total for item in self.order_items.all()])

    @property
    def items(self) -> QuerySet["OrderItem"]:
        return self.order_items.all()

    def __str__(self):
        return f'Заказ пользователя {self.user.username}'

    def save(self, *args, **kwargs):
        if self.status == self.Status.NEW:
            existing_order = Order.objects.filter(user=self.user, status=self.Status.NEW).exclude(pk=self.pk)
            if existing_order.exists():
                raise ValidationError("Пользователь имеет неподтвержденный заказ.")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        related_name="order_items",
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        related_name="product_orderitems",
        on_delete=models.CASCADE
    )

    amount = models.IntegerField(verbose_name='Количество', null=False, default=1)

    @property
    def total(self) -> int:
        return self.amount * self.product.price

    # total = models.IntegerField(verbose_name="Цена")

    def __str__(self):
        return f'Элемент заказа {self.order.pk}'

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказов'
        constraints = [
            CheckConstraint(check=Q(amount__gte=1), name="order_amount_more_than_0"),
        ]
