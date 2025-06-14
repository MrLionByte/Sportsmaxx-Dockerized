from django.urls import path, include
from . import views


auth_patterns = [
    path("sign-in/", views.user_sign_in, name="user_sign_in"),
    path("sign-up/", views.user_sign_up, name="user_sign_up"),
    path("logout/", views.user_logout, name="user_logout"),
]

otp_patterns = [
    path("register/", views.otp_reg, name="otp_reg"),
    path("email-generator/", views.email_otp_generator, name="email_otp_generator"),
    path("resend/", views.resend_otp, name="resend_otp"),
]

forgot_password_patterns = [
    path("email/", views.forgot_password_email, name="forgot_password_email"),
    path("", views.forgot_password, name="forgot_password"),
    path("otp/", views.forgot_password_otp, name="forgot_password_otp"),
]

urlpatterns = [
    path("auth/", include((auth_patterns, "auth"))),
    path("otp/", include((otp_patterns, "otp"))),
    path("forgot-password/", include((forgot_password_patterns, "forgot_password"))),
]