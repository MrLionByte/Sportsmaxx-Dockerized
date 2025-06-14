from django.urls import path
from coupons_app import views


urlpatterns = [
    path("", views.admin_coupons, name="admin_coupons"),
    path("add/", views.admin_coupon_add, name="admin_coupon_add"),
    path("expired/", views.coupons_expired, name="coupons_expired"),
    path("list/<int:coupon_id>/", views.coupon_list, name="coupon_list"),
    path("unlist/<int:coupon_id>/", views.coupon_un_list, name="coupon_un_list"),
    path("edit/<int:coupon_id>/", views.edit_coupon, name="edit_coupon"),
]
