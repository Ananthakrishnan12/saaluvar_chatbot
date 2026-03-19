# from fastapi import APIRouter, Request
# from services.appointment_service import book_appointment_api
# from chatbot.chatbot_flow import process_message, chat_sessions, ChatbotState
# from datetime import datetime
# import uuid

# router = APIRouter()


# @router.post("/chat")
# async def chatbot(request: Request):

#     body = await request.json()

#     user_id = body.get("user_id")
#     message = body.get("message")

#     patient_name = body.get("patientName")
#     patient_key = body.get("patientKey")
#     patient_mobile = body.get("patientMobile")
#     clinic = body.get("clinic")

#     # --------------------------------------------
#     # INITIAL CALL (NO MESSAGE)
#     # --------------------------------------------
#     if not message:

#         user_id = str(uuid.uuid4())

#         chat_sessions[user_id] = ChatbotState()
#         session = chat_sessions[user_id]

#         session.data["patientName"] = patient_name
#         session.data["patientKey"] = patient_key
#         session.data["patientMobile"] = patient_mobile
#         session.data["clinic"] = clinic

#         session.step = "confirm_booking"

#         return {
#             "status": True,
#             "message": "success",
#             "data": {
#                 "user_id": user_id,
#                 "bot": f"Hi {patient_name} 👋\nHow can I help you today?\nWould you like to book an appointment?",
#                 "input": "select",
#                 "options": [
#                     {"label": "Yes", "value": "yes"},
#                     {"label": "No", "value": "no"}
#                 ]
#             }
#         }

#     # --------------------------------------------
#     # NORMAL FLOW
#     # --------------------------------------------
#     reply = process_message(user_id, message)
#     session = chat_sessions.get(user_id)

#     # --------------------------------------------
#     # 🚀 FINAL BOOKING HANDLER
#     # --------------------------------------------
#     if reply == "BOOK_APPOINTMENT":

#         try:
#             date_str = session.data.get("appointmentDate")

#             formatted_date = datetime.strptime(
#                 date_str, "%d-%b-%Y"
#             ).strftime("%d %b %Y")

#         except:
#             return {
#                 "status": False,
#                 "message": "invalid_date_format",
#                 "data": {
#                     "bot": "Invalid appointment date format."
#                 }
#             }

#         payload = {
#             "clinic": session.data.get("clinic"),
#             "doctor": session.data.get("doctor"),
#             "patientKey": session.data.get("patientKey"),
#             "patientName": session.data.get("patientName"),
#             "patientMobile": session.data.get("patientMobile"),
#             "appointmentType": session.data.get("appointmentType"),
#             "treatmentType": session.data.get("treatmentType"),
#             "visitReason": session.data.get("visitReason"),
#             "appointmentDate": formatted_date,
#             "selectedSlot": session.data.get("selectedSlot"),
#             "bookedBy": "AG9f26eafa-6227-416f-9c33-b268b45f9742",
#             "bookingType": "Online"
#         }

#         api_response = book_appointment_api(payload)

#         chat_sessions.pop(user_id, None)

#         if api_response.get("success"):

#             return {
#                 "status": True,
#                 "message": "appointment_booked",
#                 "data": {
#                     "user_id": user_id,
#                     "bot": "✅ Appointment booked successfully",
#                     "appointment_details": api_response.get("data")
#                 }
#             }

#         return {
#             "status": False,
#             "message": "appointment_failed",
#             "data": {
#                 "user_id": user_id,
#                 "bot": "❌ Appointment booking failed",
#                 "error": api_response
#             }
#         }

#     # --------------------------------------------
#     # OPTIONS HANDLING
#     # --------------------------------------------
#     options = None

#     if session:

#         if session.step in ["confirm_booking", "confirm"]:
#             options = [
#                 {"label": "Yes", "value": "yes"},
#                 {"label": "No", "value": "no"}
#             ]

#         # elif session.step == "select_doctor":
#         #     options = [
#         #         {"label": d["emp_name"], "value": str(i+1)}
#         #         for i, d in enumerate(session.data.get("doctor_list", []))
#         #     ]

#         BASE_IMAGE_URL = "https://tsitfilemanager.in/praveendurai/saaluvar-backend/public/"

#     elif session.step == "select_doctor":
#         options = []

#         for i, d in enumerate(session.data.get("doctor_list", [])):

#             emp_img = d.get("emp_img")

#             if emp_img:
#                 if emp_img.startswith("http"):
#                     final_image = emp_img
#                 else:
#                     final_image = BASE_IMAGE_URL + emp_img
#             else:
#                 final_image = "https://via.placeholder.com/150"

#             options.append({
#                 "label": d["emp_name"],
#                 "value": str(i+1),
#                 "image": final_image
#             })
#             ]

#         elif session.step == "select_date":
#             options = [
#                 {"label": d, "value": str(i+1)}
#                 for i, d in enumerate(session.data.get("date_list", []))
#             ]

#         elif session.step == "select_slot":
#             options = [
#                 {"label": s, "value": str(i+1)}
#                 for i, s in enumerate(session.data.get("slot_list", []))
#             ]

#         elif session.step == "appointment_type":
#             options = [
#                 {"label": "New", "value": "new"},
#                 {"label": "Follow Up", "value": "follow up"}
#             ]

#         elif session.step == "select_treatment":
#             options = [
#                 {"label": t["service_name"], "value": str(i+1)}
#                 for i, t in enumerate(session.data.get("treatment_list", []))
#             ]

#     # --------------------------------------------
#     # FINAL RESPONSE FORMAT
#     # --------------------------------------------
#     response_data = {
#         "user_id": user_id,
#         "bot": reply
#     }

#     if options:
#         response_data["input"] = "select"
#         response_data["options"] = options
#     else:
#         response_data["input"] = "textfield"

#     return {
#         "status": True,
#         "message": "success",
#         "data": response_data
#     }


from fastapi import APIRouter, Request
from services.appointment_service import book_appointment_api
from chatbot.chatbot_flow import process_message, chat_sessions, ChatbotState
from datetime import datetime
import uuid

router = APIRouter()

BASE_IMAGE_URL = "https://tsitfilemanager.in/praveendurai/saaluvar-backend/public/"


@router.post("/chat")
async def chatbot(request: Request):

    body = await request.json()

    user_id = body.get("user_id")
    message = body.get("message")

    patient_name = body.get("patientName")
    patient_key = body.get("patientKey")
    patient_mobile = body.get("patientMobile")
    clinic = body.get("clinic")

    # --------------------------------------------
    # INITIAL CALL (NO MESSAGE)
    # --------------------------------------------
    if not message:

        user_id = str(uuid.uuid4())

        chat_sessions[user_id] = ChatbotState()
        session = chat_sessions[user_id]

        session.data["patientName"] = patient_name
        session.data["patientKey"] = patient_key
        session.data["patientMobile"] = patient_mobile
        session.data["clinic"] = clinic

        session.step = "confirm_booking"

        return {
            "status": True,
            "message": "success",
            "data": {
                "user_id": user_id,
                "bot": f"Hi {patient_name} 👋\nHow can I help you today?\nWould you like to book an appointment?",
                "input": "select",
                "options": [
                    {"label": "Yes", "value": "yes"},
                    {"label": "No", "value": "no"}
                ]
            }
        }

    # --------------------------------------------
    # NORMAL FLOW
    # --------------------------------------------
    reply = process_message(user_id, message)
    session = chat_sessions.get(user_id)

    # --------------------------------------------
    # FINAL BOOKING HANDLER
    # --------------------------------------------
    if reply == "BOOK_APPOINTMENT":

        try:
            date_str = session.data.get("appointmentDate")

            formatted_date = datetime.strptime(
                date_str, "%d-%b-%Y"
            ).strftime("%d %b %Y")

        except:
            return {
                "status": False,
                "message": "invalid_date_format",
                "data": {
                    "bot": "Invalid appointment date format."
                }
            }

        payload = {
            "clinic": session.data.get("clinic"),
            "doctor": session.data.get("doctor"),
            "patientKey": session.data.get("patientKey"),
            "patientName": session.data.get("patientName"),
            "patientMobile": session.data.get("patientMobile"),
            "appointmentType": session.data.get("appointmentType"),
            "treatmentType": session.data.get("treatmentType"),
            "visitReason": session.data.get("visitReason"),
            "appointmentDate": formatted_date,
            "selectedSlot": session.data.get("selectedSlot"),
            "bookedBy": "AG9f26eafa-6227-416f-9c33-b268b45f9742",
            "bookingType": "Online"
        }

        api_response = book_appointment_api(payload)

        chat_sessions.pop(user_id, None)

        if api_response.get("success"):
            return {
                "status": True,
                "message": "appointment_booked",
                "data": {
                    "user_id": user_id,
                    "bot": "✅ Appointment booked successfully",
                    "appointment_details": api_response.get("data")
                }
            }

        return {
            "status": False,
            "message": "appointment_failed",
            "data": {
                "user_id": user_id,
                "bot": "❌ Appointment booking failed",
                "error": api_response
            }
        }

    # --------------------------------------------
    # OPTIONS HANDLING
    # --------------------------------------------
    options = None

    if session:

        # YES / NO
        if session.step in ["confirm_booking", "confirm"]:
            options = [
                {"label": "Yes", "value": "yes"},
                {"label": "No", "value": "no"}
            ]

        # DOCTOR WITH IMAGE ✅
        elif session.step == "select_doctor":
            options = []

            for i, d in enumerate(session.data.get("doctor_list", [])):

                emp_img = d.get("emp_img")

                if emp_img:
                    if emp_img.startswith("http"):
                        final_image = emp_img
                    else:
                        final_image = BASE_IMAGE_URL + emp_img
                else:
                    final_image = "https://via.placeholder.com/150"

                options.append({
                    "label": d["emp_name"],
                    "value": str(i+1),
                    "image": final_image
                })

        # DATE
        elif session.step == "select_date":
            options = [
                {"label": d, "value": str(i+1)}
                for i, d in enumerate(session.data.get("date_list", []))
            ]

        # SLOT
        elif session.step == "select_slot":
            options = [
                {"label": s, "value": str(i+1)}
                for i, s in enumerate(session.data.get("slot_list", []))
            ]

        # APPOINTMENT TYPE
        elif session.step == "appointment_type":
            options = [
                {"label": "New", "value": "new"},
                {"label": "Follow Up", "value": "follow up"}
            ]

        # TREATMENT
        elif session.step == "select_treatment":
            options = [
                {"label": t["service_name"], "value": str(i+1)}
                for i, t in enumerate(session.data.get("treatment_list", []))
            ]

    # --------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------
    response_data = {
        "user_id": user_id,
        "bot": reply
    }

    if options:
        response_data["input"] = "select"
        response_data["options"] = options
    else:
        response_data["input"] = "textfield"

    return {
        "status": True,
        "message": "success",
        "data": response_data
    }