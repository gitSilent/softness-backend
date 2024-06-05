from django.contrib import admin

from .models import Category, Product, ProductPhoto

# Register your models here.

class ProductPhotoInline(admin.TabularInline):
    model = ProductPhoto
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPhotoInline]
    list_display = ('title', 'price', 'category')
    search_fields = ('title', 'desc')
    list_filter = ('category',)


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
