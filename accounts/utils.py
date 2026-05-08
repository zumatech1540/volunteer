import requests
from django.conf import settings
import africastalking
from django.conf import settings

def send_whatsapp_message(phone, message):

    url = f"https://graph.facebook.com/v19.0/{settings.WHATSAPP_PHONE_ID}/messages"

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()

from django.shortcuts import redirect
from functools import wraps


# ================= ADMIN ONLY =================
def admin_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)

        return redirect('home')

    return wrapper


# ================= LEADER ONLY =================
def leader_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated and request.user.role == 'leader':
            return view_func(request, *args, **kwargs)

        return redirect('home')

    return wrapper


# ================= VOLUNTEER ONLY =================
def volunteer_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated and request.user.role == 'volunteer':
            return view_func(request, *args, **kwargs)

        return redirect('home')

    return wrapper



# Initialize SDK
username = settings.AFRICASTALKING_USERNAME
api_key = settings.AFRICASTALKING_API_KEY

africastalking.initialize(username, api_key)

sms = africastalking.SMS


def send_sms(phone_numbers, message):

    try:
        response = sms.send(
            message,
            phone_numbers
        )

        return response

    except Exception as e:
        print("SMS Error:", e)
        return None