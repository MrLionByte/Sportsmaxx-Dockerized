from django.urls import path, include
from . import views

my_account_patterns = [
    path("", views.user_profile, name="my_account"),
    path("add-account-address/", views.add_account_address, name="add_account_address"),
    path("delete-address/<int:address_id>/", views.delete_address, name="delete_address"),
    path("edit-address/<int:address_id>/", views.edit_address, name="edit_address"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("change-password/", views.change_password, name="change_password"),
]

checkout_address_patterns = [
    path("add-checkout-address/", views.add_checkout_address, name="add_checkout_address"),
    path("edit-checkout-address/<int:address_id>/", views.edit_checkout_address, name="edit_checkout_address"),
]

urlpatterns = [
    path("user-account-details/<int:user_id>/", views.user_account_details_admin, name="user_account_details_admin"),
    path("my-account/", include((my_account_patterns))),
    path("checkout/", include((checkout_address_patterns))),
]
