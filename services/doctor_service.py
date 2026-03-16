import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("base_url")
TOKEN = os.getenv("CLINIC_API_TOKEN")

DOCTOR_CATEGORY = "DOC9ea5fc7d-bca3-451e-8f18-df073af79abf"
CLINIC_KEY = "CLC9ea06fe8-f541-4123-8886-3569fe359b0a"


def get_doctors():

    url = BASE_URL + "getEmpByCat"

    payload = {
        "emp_cat_key": DOCTOR_CATEGORY,
        "per_page": 10,
        "page": 1,
        "clinic_key": CLINIC_KEY
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