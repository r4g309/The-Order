from django.urls import path
from . import views

urlpatterns = [
    path("", views.create_shopping_cart, name="create_order"),
    path("<int:cart_id>/add", views.add_to_cart, name="add_to_cart"),
    path("<int:cart_id>/remove/<int:item_id>", views.remove_item, name="remove_item"),
    path("<int:cart_id>/checkout/", views.checkout, name="checkout"),
    path("list/", views.list_orders, name="list_orders"),
    path("<int:cart_id>/confirm/", views.update_order_state, name="change_state"),
    path("product/add/", views.add_product, name="add_product"),
]
