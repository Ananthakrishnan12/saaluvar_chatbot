from fastapi import APIRouter, Request
from schemas.appointment_schema import AppointmentRequest
from services.appointment_service import book_appointment_api
from chatbot.chatbot_flow import process_message, chat_sessions
from datetime import datetime
import uuid

router = APIRouter()


# ---------------------------------------------------
# Existing direct appointment API (NO CHANGE)
# ---------------------------------------------------

@router.post("/bookappointment")
def book_appointment(payload: AppointmentRequest):

    payload_dict = payload.dict()

    result = book_appointment_api(payload_dict)

    return result


# ---------------------------------------------------
# Chatbot API
# ---------------------------------------------------

@router.post("/chat")
async def chatbot(request: Request):

    body = await request.json()

    user_id = body.get("user_id")
    message = body.get("message")

    if not message:
        return {"error": "message is required"}

    # Generate user_id for first request
    if not user_id:
        user_id = str(uuid.uuid4())

    # Process chatbot flow
    reply = process_message(user_id, message)

    session = chat_sessions.get(user_id)

    # ---------------------------------------------------
    # FINAL STEP → Confirm booking
    # ---------------------------------------------------

    if session and session.step == "confirm" and message.lower() == "yes":

        try:
            date_str = session.data.get("appointmentDate")

            formatted_date = datetime.strptime(
                date_str, "%d-%b-%Y"
            ).strftime("%d %b %Y")

        except:
            return {
                "bot": "Invalid appointment date format."
            }

        # ----------------------------------------------
        # Create Appointment Payload
        # ----------------------------------------------

        payload = {
            "clinic": "CLC9ea06fe8-f541-4123-8886-3569fe359b0a",
            "doctor": session.data.get("doctor"),

            # Temporary fallback values
            "patientKey": session.data.get("patientKey") or "9fefbaa7-a165-42ee-9b7e-ad4922dfce4f",
            "patientName": session.data.get("patientName") or "Test Patient",
            "patientMobile": session.data.get("patientMobile") or "9876543210",

            "appointmentType": session.data.get("appointmentType"),
            "treatmentType": session.data.get("treatmentType"),
            "visitReason": session.data.get("visitReason"),
            "appointmentDate": formatted_date,
            "selectedSlot": session.data.get("selectedSlot"),
            "bookedBy": "AG9f26eafa-6227-416f-9c33-b268b45f9742",
            "bookingType": "Online"
        }

        # Clear session after collecting data
        chat_sessions.pop(user_id, None)

        # ----------------------------------------------
        # RETURN APPOINTMENT REQUEST (not booking yet)
        # ----------------------------------------------

        return {
            "bot": "Appointment details collected successfully",
            "appointment_request": payload
        }

    # ---------------------------------------------------
    # Continue chatbot conversation
    # ---------------------------------------------------

    return {
        "user_id": user_id,
        "bot": reply
    }