import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("base_url")
TOKEN = os.getenv("CLINIC_API_TOKEN")

ENDPOINT = "bookappointment"

def book_appointment_api(payload: dict):

    url = BASE_URL + ENDPOINT

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()