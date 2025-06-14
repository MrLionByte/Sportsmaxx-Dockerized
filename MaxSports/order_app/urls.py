from django.urls import path, include
from order_app import views

# Admin URLs
admin_order_patterns = [
    path("", views.admin_order, name="order_processing"),
    path("delivered/", views.admin_delivered, name="order_delivered"),
    path("pending-actions/", views.admin_pending_actions, name="admin_pending_actions"),
    path("edit/<int:order_id>/", views.admin_edit_order, name="admin_edit_order"),
    path("details/<int:order_id>/", views.order_details, name="order_details"),
    path("status-change/", views.order_status_change, name="order_status_change"),
    path("confirmation/<int:order_id>/", views.order_confirmation, name="order_confirmation"),
    path("cancel-approval/<int:order_id>/", views.order_cancel_approval, name="order_cancel_approval"),
]

# Report URLs
report_patterns = [
    path("pdf/", views.download_report_in_pdf, name="download_report_in_pdf"),
    path("excel/", views.sales_report_excel, name="sales_report_excel"),
]

# Invoice URLs
invoice_patterns = [
    path("<int:serial_number>/", views.order_invoice, name="order_invoice"),
    path("download/<int:serial_number>/", views.download_invoice, name="download_invoice"),
]

# User URLs
user_order_patterns = [
    path("", views.user_orders, name="user_orders"),
    path("confirm/", views.order_confirm, name="order_confirm"),
    path("checkout/add/", views.add_to_order, name="add_to_order"),
    path("orders/<int:order_id>/", views.user_order_details, name="user_order_details"),
    path("cancel/<int:order_id>/", views.cancel_order, name="cancel_order"),
    path("re-order-payment/", views.re_order_payment, name="re_order_payment"),
]

urlpatterns = [
    path("admin/orders/", include((admin_order_patterns, "admin_order"))),
    path("admin/reports/", include((report_patterns, "reports"))),
    path("invoice/", include((invoice_patterns, "invoice"))),
    path("user/orders/", include((user_order_patterns, "user_order"))),
]