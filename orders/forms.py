# Create a form for user to fill in their order details

from django import forms
from .models import ShoppingCart, ShoppingCartItem, Product


class ShoppingCartForm(forms.ModelForm):
    class Meta:
        model = ShoppingCart
        fields = ["name", "items", "in_site"]
        widgets = {
            "items": forms.CheckboxSelectMultiple,
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese su nombre",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 "
                             "focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "in_site": forms.RadioSelect(
                choices=[(True, "En sitio"), (False, "Para llevar")],
                attrs={"class": "ms-2 text-sm font-medium text-gray-900 text-2xl"},
            ),
        }


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = ShoppingCartItem
        fields = ["product", "quantity", "observation"]
        widgets = {
            "product": forms.Select(
                choices=Product.objects.all(),
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 "
                             "focus:border-blue-500 block w-full p-2.5"
                },
            ),
            "observation": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 "
                             "focus:ring-blue-500 focus:border-blue-500",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "min": "1",
                    "value": "1",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 "
                             "focus:border-blue-500 block w-full p-2.5",
                }
            ),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Ingrese el nombre del producto"}
            ),
            "price": forms.NumberInput(
                attrs={"placeholder": "Ingrese el precio del producto"}
            ),
            "description": forms.Textarea(
                attrs={"placeholder": "Ingrese la descripcion del producto"}
            ),
        }
