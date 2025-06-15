from django.urls import path, include
from . import views

cart_patterns = [
    path("", views.cart_show, name="cart_show"),
    path("add/", views.add_product_to_cart, name="add_product_to_cart"),
    path("remove/", views.remove_from_cart, name="remove_from_cart"),
    path("update-total/", views.update_total_price, name="update_total_price"),
]

coupon_patterns = [
    path("apply/", views.apply_coupon, name="apply_coupon"),
    path("delete/", views.delete_coupon, name="delete_coupon"),
]

wishlist_patterns = [
    path("", views.show_wishlist, name="show_wishlist"),
    path("add/<int:product_id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("delete/", views.delete_from_wishlist, name="delete_from_wishlist"),
]

urlpatterns = [
    path("cart/", include((cart_patterns))),
    path("coupon/", include((coupon_patterns))),
    path("checkout/", views.checkout_product, name="checkout_product"),
    path("wishlist/", include((wishlist_patterns))),
]