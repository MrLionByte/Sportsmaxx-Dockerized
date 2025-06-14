from django.urls import path
from Admin_side_app import views

urlpatterns = [
    path("login/", views.admin_login, name="admin_login"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("next-page/", views.admin_dashboard_page, name="admin_dashboard_page"),
    path(
        "user-management/",
        views.admin_user_management,
        name="admin_user_management",
    ),
    path(
        "user-management/unlisted/",
        views.admin_user_management_unlisted,
        name="admin_user_management_unlisted",
    ),
    path(
        "user-block/<int:user_id>/", views.user_action_block, name="user_action_block"
    ),
    path(
        "user-unblock/<int:user_id>/",
        views.user_action_unblock,
        name="user_action_unblock",
    ),
    path("logout/", views.admin_logout, name="admin_logout"),
]
