from django.urls import path
from . import views

urlpatterns = [
    path("pay/", views.payment_page, name="payment_page"),
    path("pay/confirm/", views.payment_confirm, name="payment_confirm"),
    path("pay/success/", views.payment_success, name="payment_success"),
]
