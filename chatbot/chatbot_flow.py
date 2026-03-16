import uuid
from services.doctor_service import get_doctors
from services.slot_service import get_available_dates, get_available_slots
from services.treatment_service import get_treatment_types
from datetime import datetime, timedelta


class ChatbotState:
    def __init__(self):
        self.step = "confirm_booking"
        self.data = {}


chat_sessions = {}



def generate_dates():

    dates = []

    today = datetime.today()

    for i in range(7):
        day = today + timedelta(days=i)
        dates.append(day.strftime("%d-%b-%Y"))

    return dates


def process_message(user_id, message):

    # Start conversation
    if not user_id:

        user_id = str(uuid.uuid4())

        chat_sessions[user_id] = ChatbotState()

        return {
            "user_id": user_id,
            "bot": "Hello 👋 I can help you book an appointment. Would you like to continue? (yes/no)"
        }

    # Session expired
    if user_id not in chat_sessions:

        if message.lower() in ["hi", "hello", "hey"]:

            chat_sessions[user_id] = ChatbotState()

            return "Hello 👋 I can help you book an appointment.\nWould you like to continue? (yes/no)"

        else:
            return "Please start by saying 'hi'."

    session = chat_sessions[user_id]

    # Debug logs
    print("USER:", user_id)
    print("STEP:", session.step)
    print("MESSAGE:", message)

    # --------------------------------------------------
    # Confirm booking
    # --------------------------------------------------
    if session.step == "confirm_booking":

        if message.lower() != "yes":
            return {
                "user_id": user_id,
                "bot": "Okay. Let me know if you need help later."
            }

        session.step = "visit_reason"

        return {
            "user_id": user_id,
            "bot": "Please tell the reason for your visit."
        }

    # --------------------------------------------------
    # Visit reason
    # --------------------------------------------------
    if session.step == "visit_reason":

        session.data["visitReason"] = message

        doctors = get_doctors()

        if not doctors:
            return {
                "user_id": user_id,
                "bot": "No doctors available."
            }

        session.data["doctor_list"] = doctors
        session.step = "select_doctor"

        text = "Available Doctors:\n"

        for i, doc in enumerate(doctors):
            text += f"{i+1}. {doc['emp_name']}\n"

        text += "\nSelect doctor number."

        return {
            "user_id": user_id,
            "bot": text
        }

    # --------------------------------------------------
    # Select doctor
    # --------------------------------------------------
    if session.step == "select_doctor":

        doctors = session.data["doctor_list"]

        try:
            index = int(message) - 1
            doctor = doctors[index]
        except:
            return {
                "user_id": user_id,
                "bot": "Invalid doctor selection."
            }

        session.data["doctor"] = doctor["emp_key"]

        # 🔹 Call Date API
        dates = generate_dates()

        # If no dates available
        if not dates:

            doctors = session.data["doctor_list"]

            text = "❌ No available dates for this doctor.\n\nPlease choose another doctor:\n"

            for i, doc in enumerate(doctors):
                text += f"{i+1}. {doc['emp_name']}\n"

            text += "\nSelect doctor number."

            session.step = "select_doctor"

            return {
                "user_id": user_id,
                "bot": text
            }

        session.data["date_list"] = dates
        session.step = "select_date"

        text = "Available Dates:\n"

        for i, d in enumerate(dates):
            text += f"{i+1}. {d}\n"

        text += "\nSelect date number."

        return {
            "user_id": user_id,
            "bot": text
        }

    # --------------------------------------------------
    # Select date
    # --------------------------------------------------
    if session.step == "select_date":

        dates = session.data["date_list"]

        try:
            index = int(message) - 1
            selected_date = dates[index]
        except:
            return "Invalid date selection."

        session.data["appointmentDate"] = selected_date

        slots = get_available_slots(session.data["doctor"], selected_date)

        if not slots:

            text = "No slots available for this date.\n\nPlease choose another date:\n"

            for i, d in enumerate(dates):
                text += f"{i+1}. {d}\n"

            text += "\nSelect date number."

            return text

        session.data["slot_list"] = slots
        session.step = "select_slot"

        text = "Available Slots:\n"

        for i, slot in enumerate(slots):
            text += f"{i+1}. {slot}\n"

        text += "\nSelect slot number."

        return text


    # --------------------------------------------------
    # Select slot
    # --------------------------------------------------
    if session.step == "select_slot":

        slots = session.data["slot_list"]

        try:
            index = int(message) - 1
            slot = slots[index]
        except:
            return {
                "user_id": user_id,
                "bot": "Invalid slot selection."
            }

        session.data["selectedSlot"] = slot

        session.step = "appointment_type"

        return {
            "user_id": user_id,
            "bot": "Appointment type? (New / Follow Up)"
        }

    # --------------------------------------------------
    # Appointment type
    # --------------------------------------------------
    if session.step == "appointment_type":

        session.data["appointmentType"] = message

        services = get_treatment_types()

        session.data["treatment_list"] = services
        session.step = "select_treatment"

        text = "Available Treatment Types:\n"

        for i, service in enumerate(services):
            text += f"{i+1}. {service['service_name']}\n"

        text += "\nSelect treatment number."

        return {
            "user_id": user_id,
            "bot": text
        }

    # --------------------------------------------------
    # Select treatment
    # --------------------------------------------------
    if session.step == "select_treatment":

        services = session.data["treatment_list"]

        try:
            index = int(message) - 1
            service = services[index]
        except:
            return {
                "user_id": user_id,
                "bot": "Invalid treatment selection."
            }

        session.data["treatmentType"] = service["service_name"]

        session.step = "confirm"

        return {
            "user_id": user_id,
            "bot": "Confirm appointment booking? (yes/no)"
        }

    return {
        "user_id": user_id,
        "bot": f"Unhandled step: {session.step}"
    }