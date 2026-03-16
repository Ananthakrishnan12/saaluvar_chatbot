import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("base_url")
TOKEN = os.getenv("CLINIC_API_TOKEN")


CLINIC_KEY = "CLC9ea06fe8-f541-4123-8886-3569fe359b0a"


def get_treatment_types():

    url = BASE_URL + "hospital/getHospitalServices"

    payload = {
        "hospital_key": CLINIC_KEY
    }

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    if data.get("success"):
        return data["data"]

    return []