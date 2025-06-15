from django.urls import path, include
from product_app import views

# Admin product URLs
admin_product_patterns = [
    path("", views.admin_product, name="admin_product"),
    path("unlisted/", views.admin_product_unlisted, name="admin_product_unlisted"),
    path("add/", views.admin_add_product, name="admin_add_product"),
    path("details/<int:product_id>/", views.admin_details_product, name="admin_details_product"),
    path("edit/<int:product_id>/", views.admin_edit_product, name="admin_edit_product"),
    path("feature/<int:product_id>/", views.feature, name="feature"),
    path("unfeature/<int:product_id>/", views.unfeature, name="unfeature"),
    path("edit-variant/", views.admin_edit_variant, name="admin_edit_variant"),
    path("edit-image/<int:product_id>/", views.edit_product_image, name="edit_product_image"),
    path("edit-variant/<int:product_id>/", views.admin_edit_variant, name="admin_edit_variant"),
    path("add-size-qty/", views.admin_add_size_qty, name="admin_add_size_qty"),
    path("edit-size-qty/<int:product_id>/", views.admin_edit_size_qty, name="admin_edit_size_qty"),
    path("list/<int:product_id>/", views.admin_list_product, name="admin_list_product"),
    path("unlist/<int:product_id>/", views.admin_unlist_product, name="admin_unlist_product"),
    path("status/list/<int:product_id>/", views.admin_productStatus_list, name="admin_productStatus_list"),
    path("status/unlist/<int:product_id>/", views.admin_productStatus_unlist, name="admin_productStatus_unlist"),
]

# Admin color/type URLs
admin_color_patterns = [
    path("list/<int:product_id>/", views.product_color_list, name="list_product_type"),
    path("unlist/<int:product_id>/", views.product_color_unlist, name="unlist_product_type"),
    path("delete/<int:product_id>/", views.product_color_delete, name="product_color_delete"),
    path("undo/<int:product_id>/", views.product_color_undo, name="product_color_undo"),
]

# User product URLs
user_product_patterns = [
    path("all/", views.all_products_list, name="all_products_list"),
    path("<int:products_id>/", views.user_products, name="user_products"),
    path("details/<int:products_id>/", views.product_details, name="product_details"),
]

urlpatterns = [
    path("admin/products/", include((admin_product_patterns))),
    path("admin/products/colors/", include((admin_color_patterns))),
    path("user/products/", include((user_product_patterns))),
]



