import requests
import json
from django.conf import settings


def publish_to_centrifugo(channel, data):
    try:
        url = f"{settings.CENTRIFUGO_API_URL}/publish"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"apikey {settings.CENTRIFUGO_API_KEY}"
        }
        payload = {
            "channel": channel,
            "data": data
        }
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Centrifugo publish error: {e}")
        return False
