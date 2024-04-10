from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from .views import home_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("orders/", include("orders.urls")),
    path("", home_page, name="home"),
]
