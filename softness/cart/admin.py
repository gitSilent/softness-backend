from django.contrib import admin

from cart.models import Cart, CartItem
from users.models import FavoriteList, FavoriteItem

# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)
