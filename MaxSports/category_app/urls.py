from django.urls import path,include
from category_app import views


admin_category_patterns = [
    path("", views.admin_category, name="admin_category"),
    path("unlisted/", views.admin_category_unlisted, name="admin_category_unlisted"),
    path("add/", views.admin_add_category, name="admin_add_category"),
    path("edit/<int:category_id>/", views.admin_edit_category, name="admin_edit_category"),
    path("delete/<int:category_id>/", views.admin_delete_category, name="admin_delete_category"),
    path("undo/<int:category_id>/", views.admin_undo_category, name="admin_undo_category"),
    path("list/<int:category_id>/", views.admin_List_category, name="admin_List_category"),
    path("unlist/<int:category_id>/", views.admin_UnList_category, name="admin_UnList_category"),
]

admin_types_patterns = [
    path("", views.admin_types_for_category, name="admin_types_for_category"),
    path("add/", views.admin_add_types_for_category, name="admin_add_types_for_category"),
]

urlpatterns = [
    path("", include((admin_category_patterns, "admin_category"))),
    path("types/", include((admin_types_patterns, "admin_types_for_category"))),
]