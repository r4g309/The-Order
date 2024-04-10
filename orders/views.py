from datetime import datetime, timezone

from django.http import QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import ShoppingCartForm, AddToCartForm, ProductForm

from .models import ShoppingCart, OrderState


def create_shopping_cart(request):
    if request.method == "POST":
        form = ShoppingCartForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_to_cart", cart_id=form.instance.id)
    form = ShoppingCartForm()
    return render(
        request,
        "order/order.html",
        context={
            "form": form,
        },
    )


def add_to_cart(request, cart_id):
    try:
        shopping_cart = ShoppingCart.objects.get(pk=cart_id)
        if shopping_cart.state != OrderState.CREATED:
            return redirect("create_order")
    except ShoppingCart.DoesNotExist:
        return redirect("create_order")

    if request.method == "POST":
        form = AddToCartForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.shopping_car = shopping_cart
            instance.save()
            shopping_cart.items.add(instance)
            shopping_cart.save()
            return redirect("add_to_cart", cart_id=cart_id)

    context = {
        "form": AddToCartForm(),
        "cart_id": cart_id,
        "added_products": ShoppingCart.objects.get(pk=cart_id).items.all(),
        "total": shopping_cart.total,
        "in_site": shopping_cart.in_site,
        "name": shopping_cart.name,
    }
    return render(request, "order/add_to_cart.html", context=context)


def remove_item(request, cart_id, item_id):
    try:
        shopping_cart = ShoppingCart.objects.get(pk=cart_id)
        if shopping_cart.state != OrderState.CREATED:
            return redirect("create_order")
    except ShoppingCart.DoesNotExist:
        return redirect("create_order")
    try:
        item = shopping_cart.items.get(pk=item_id)
        item.delete()
        shopping_cart.save()
    except ShoppingCart.DoesNotExist:
        pass

    return redirect("add_to_cart", cart_id=cart_id)


def checkout(request, cart_id):
    # TODO: Optimze this for only pass the shopping_cart object
    redirect_after_checkout = request.GET.get("redirect", "True")
    try:
        shopping_cart = ShoppingCart.objects.get(pk=cart_id)
    except ShoppingCart.DoesNotExist:
        return redirect("create_order")
    if shopping_cart.state == OrderState.CREATED:
        shopping_cart.state = OrderState.ON_HOLD
        shopping_cart.created_at = datetime.now(timezone.utc)
        shopping_cart.save()

    return render(
        request,
        "order/checkout.html",
        context={
            "cart": shopping_cart,
            "redirect": redirect_after_checkout == "True",
            "items": [
                {
                    "name": item.product.name,
                    "quantity": item.quantity,
                    "price": item.product.price,
                    "item_total": item.item_total,
                }
                for item in shopping_cart.items.all()
            ],
        },
    )


def list_orders(request):
    return render(
        request,
        "order/list_orders.html",
        context={
            "orders": ShoppingCart.objects.all().exclude(state=OrderState.CREATED),
            "states": OrderState,
        },
    )


def update_order_state(request, cart_id):
    try:
        shopping_cart = ShoppingCart.objects.get(pk=cart_id)
    except ShoppingCart.DoesNotExist:
        return redirect("create_order")
    if shopping_cart.state != OrderState.COMPLETED:
        shopping_cart.state = OrderState.values[shopping_cart.state + 1]
        shopping_cart.save()
    if shopping_cart.state == OrderState.COMPLETED:
        query_params = QueryDict(mutable=True)
        new_url = reverse("checkout", args=[cart_id])
        query_params["redirect"] = False
        new_url += f"?{query_params.urlencode()}"
        return redirect(new_url)

    return redirect("list_orders")


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_orders")
    form = ProductForm()

    return render(
        request,
        "order/add_product.html",
        context={
            "form": form,
        },
    )
