from django.db import models

# Create your models here.
def upload_toy_photo(instance, filename):
    return f"products/{instance.product.category.slug}/{instance.product.slug}/{filename}"

class Category(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=100,
        unique=True,
        null=False
    )
    slug = models.SlugField(
        verbose_name="Слаг",
        unique=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Product(models.Model):

    title = models.CharField(
        verbose_name="Название",
        max_length=255,
        null=False
    )
    desc = models.CharField(
        verbose_name="Описание",
        max_length=1500,
        null=True
    )
    slug = models.SlugField(
        verbose_name="Слаг",
        unique=True,
        null=False
    )
    old_price = models.IntegerField(
        verbose_name="Старая цена",
        help_text="В российских рублях",
        null=True
    )
    price = models.IntegerField(
        verbose_name="Цена",
        help_text="В российских рублях",
        null=False
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title
class ProductPhoto(models.Model):
    photo = models.ImageField(
        verbose_name="Фото товара",
        upload_to=upload_toy_photo
    )
    product = models.ForeignKey(
        Product,
        verbose_name="Связь с товаром",
        on_delete=models.CASCADE,
        related_name="photos",
        null=True
    )

    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фото товаров"