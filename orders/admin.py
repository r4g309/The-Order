from django.contrib import admin
from .models import Product, ShoppingCartItem, ShoppingCart

# Register your models here.
admin.site.register(Product)
admin.site.register(ShoppingCartItem)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    readonly_fields = ["total"]
