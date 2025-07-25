import requests
import random
from django.conf import settings


def send_otp_phone(phone_number):
    try:
        otp = random.randint(100000, 999999)
        url = f"https://2factor.in/API/V1/{settings.API_KEY}/SMS/{phone_number}/{otp}/{otp_template_name}"
        response = requests.get(url)

    except Exception:
        return None
