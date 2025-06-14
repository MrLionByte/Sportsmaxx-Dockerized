from django.urls import path, include
from offers import views


category_offer_patterns = [
    path("", views.category_offers, name="category_offers"),
    path("edit/<int:offer_id>/", views.edit_category_offers, name="edit_category_offers"),
]

product_offer_patterns = [
    path("", views.product_offers, name="product_offers"),
    path("edit/<int:offer_id>/", views.edit_product_offers, name="edit_product_offers"),
]

urlpatterns = [
    path("category-offers/", include((category_offer_patterns, "category_offers"))),
    path("product-offers/", include((product_offer_patterns, "product_offers"))),
]
