from django.contrib import admin

from .models import User, City, FavoriteItem, FavoriteList

# Register your models here.

admin.site.register(User)
admin.site.register(City)

class FavoriteItemInline(admin.TabularInline):
    model = FavoriteItem
    extra = 1  # Adjust the number of empty forms as needed
    fields = ('product',)  # Display the product field in the inline

@admin.register(FavoriteList)
class FavoriteListAdmin(admin.ModelAdmin):
    inlines = [FavoriteItemInline]
    list_display = ('user',)  # Display the user field in the list view


@admin.register(FavoriteItem)
class FavoriteItemAdmin(admin.ModelAdmin):
    list_display = ("product", "user_username")
