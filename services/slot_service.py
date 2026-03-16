from datetime import datetime, timedelta
import requests
import os

BASE_URL = os.getenv("base_url")
TOKEN = os.getenv("CLINIC_API_TOKEN")


def get_available_dates(doctor_key):

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }

    available_dates = []

    today = datetime.today()

    # check next 7 days
    for i in range(7):

        date_obj = today + timedelta(days=i)

        formatted_date = datetime.strptime(date, "%d-%b-%Y").strftime("%d-%b-%Y")

        # url = f"{BASE_URL}getAppointmentTimeslotList/{doctor_key}/{formatted_date}"

        url = f"{BASE_URL}getAppointmentTimeslotList/{doctor_key}"

        response = requests.get(url, headers=headers)

        data = response.json()

        if data.get("success") and data.get("data"):
            available_dates.append(formatted_date)

    return available_dates


# -----------------------------
# Get Available Slots
# -----------------------------
def get_available_slots(doctor_key, date):

    url = BASE_URL + f"getAppointmentTimeslotList/{doctor_key}/{date}"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }

    response = requests.post(url, headers=headers)

    data = response.json()

    print("API URL:", url)
    print("API RESPONSE:", data)

    if data.get("success"):
        return data.get("data", [])

    return []