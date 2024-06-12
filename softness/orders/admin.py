from django.contrib import admin

from orders.models import Order, OrderItem

# Register your models here.
admin.site.register(OrderItem)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Adjust the number of empty forms as needed
    fields = ('product', 'amount')  # Display the product field in the inline

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'user',)  # Display the user field in the list view
    search_fields = ['id', 'user__username']