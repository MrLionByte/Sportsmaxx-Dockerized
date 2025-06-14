from django.urls import path
from . import views

urlpatterns = [
    path("initiate/", views.initiate_payment, name="initiate_payment"),
    path("failure/", views.payment_failure, name="payment_failure"),
    path("wallet/initiate/", views.initiate_payment_for_wallet, name="initiate_payment_for_wallet"),
]
