from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_wallet, name="user_wallet"),
    path("update-balance/", views.update_wallet_balance, name="update_wallet_balance"),
]
