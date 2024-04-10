from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"


class OrderState(models.IntegerChoices):
    CREATED = (0, _("En creacion por el usuario"))
    ON_HOLD = (1, _("En espera"))
    IN_PROGRESS = (2, _("En progreso"))
    COMPLETED = (3, _("Completado"))


class ShoppingCartItem(models.Model):
    shopping_car = models.ForeignKey(
        "ShoppingCart",
        on_delete=models.CASCADE,
        related_name="items_list",
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    observation = models.TextField(null=True, blank=True)

    @property
    def item_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class ShoppingCart(models.Model):
    name = models.CharField(max_length=50)
    items = models.ManyToManyField(ShoppingCartItem, blank=True, related_name="items")
    state = models.IntegerField(choices=OrderState.choices, default=OrderState.CREATED)
    created_at = models.DateTimeField(auto_now_add=True)
    in_site = models.BooleanField(default=True)

    @property
    def total(self):
        items = self.items.all()
        if not items:
            return 0
        return sum(item.item_total for item in items)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} {self.name}"


class SiteConfig(models.Model):
    shop_name = models.CharField(max_length=100)
    shop_icon = models.ImageField(upload_to="shop_icon/")
