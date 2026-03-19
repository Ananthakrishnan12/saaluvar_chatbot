# from fastapi import APIRouter, Request
# from schemas.appointment_schema import AppointmentRequest
# from services.appointment_service import book_appointment_api
# from chatbot.chatbot_flow import process_message, chat_sessions,ChatbotState
# from datetime import datetime
# import uuid

# router = APIRouter()


# # ---------------------------------------------------
# # Existing direct appointment API (NO CHANGE)
# # ---------------------------------------------------

# @router.post("/bookappointment")
# def book_appointment(payload: AppointmentRequest):

#     payload_dict = payload.dict()

#     result = book_appointment_api(payload_dict)

#     return result



# def build_response(user_id, bot, options=None, message="success"):
#     response = {
#         "user_id": user_id,
#         "bot": bot
#     }

#     if options:
#         response["input"] = "select"
#         response["options"] = options
#     else:
#         response["input"] = "text"

#     return {
#         "status": True,
#         "message": message,
#         "data": response
#     }


# # ---------------------------------------------------
# # Chatbot API
# # ---------------------------------------------------

# @router.post("/chat")
# async def chatbot(request: Request):

#     body = await request.json()

#     user_id = body.get("user_id")
#     message = body.get("message")

#     # NEW INPUTS (from frontend/login)
#     patient_name = body.get("patientName")
#     patient_key = body.get("patientKey")
#     patient_mobile = body.get("patientMobile")
#     clinic = body.get("clinic")

#     import uuid

#     # ---------------------------------------------------
#     # FIRST REQUEST (NO MESSAGE → INIT CHAT)
#     # ---------------------------------------------------

#     if not message:

#         user_id = str(uuid.uuid4())

#         # create session
#         chat_sessions[user_id] = ChatbotState()

#         session = chat_sessions[user_id]

#         # store patient details
#         session.data["patientName"] = patient_name
#         session.data["patientKey"] = patient_key
#         session.data["patientMobile"] = patient_mobile
#         session.data["clinic"] = clinic

#         session.step = "confirm_booking"

#         reply = f"Hi {patient_name} 👋\nHow can I help you today?\nWould you like to book an appointment?"

#         options = [
#             {"label": "Yes", "value": "yes"},
#             {"label": "No", "value": "no"}
#         ]

#         return build_response(user_id, reply, options, message="hi")



#     # --------------------------------------------
#     # FINAL CONFIRM HANDLING (MOVE THIS UP)
#     # --------------------------------------------

#     session = chat_sessions.get(user_id)

#     if session and session.step == "confirm" and message.lower() == "yes":

#         from datetime import datetime

#         try:
#             date_str = session.data.get("appointmentDate")

#             formatted_date = datetime.strptime(
#                 date_str, "%d-%b-%Y"
#             ).strftime("%d %b %Y")

#         except:
#             return {"bot": "Invalid appointment date format."}

#         payload = {
#             "clinic": "CLC9ea06fe8-f541-4123-8886-3569fe359b0a",
#             "doctor": session.data.get("doctor"),
#             "patientKey": session.data.get("patientKey") or "9fefbaa7-a165-42ee-9b7e-ad4922dfce4f",
#             "patientName": session.data.get("patientName") or "Test Patient",
#             "patientMobile": session.data.get("patientMobile") or "9876543210",
#             "appointmentType": session.data.get("appointmentType"),
#             "treatmentType": session.data.get("treatmentType"),
#             "visitReason": session.data.get("visitReason"),
#             "appointmentDate": formatted_date,
#             "selectedSlot": session.data.get("selectedSlot"),
#             "bookedBy": "AG9f26eafa-6227-416f-9c33-b268b45f9742",
#             "bookingType": "Online"
#         }

#         chat_sessions.pop(user_id, None)

#         return {
#             "status": True,
#             "message": "appointment_ready",
#             "data": {
#                 "user_id": user_id,
#                 "bot": "✅ Appointment details collected successfully",
#                 "input": "text",
#                 "appointment_request": payload
#             }
#         }
    
#     # --------------------------------------------
#     # 3. NORMAL CHAT FLOW (VERY IMPORTANT)
#     # --------------------------------------------
#     reply = process_message(user_id, message)

#     session = chat_sessions.get(user_id) 
    
#     # --------------------------------------------
#     # Dynamic Options Handling
#     # --------------------------------------------

    
#     options = None 

#     # YES / NO step
#     if session and session.step in ["confirm_booking", "confirm"]:
#         options = [
#             {"label": "Yes", "value": "yes"},
#             {"label": "No", "value": "no"}
#         ]

#     # Doctor selection
#     elif session and session.step == "select_doctor":
#         doctors = session.data.get("doctor_list", [])
#         options = [
#             {"label": doc["emp_name"], "value": str(i+1)}
#             for i, doc in enumerate(doctors)
#         ]

#     # Date selection
#     elif session and session.step == "select_date":
#         dates = session.data.get("date_list", [])
#         options = [
#             {"label": d, "value": str(i+1)}
#             for i, d in enumerate(dates)
#         ]

#     # Slot selection
#     elif session and session.step == "select_slot":
#         slots = session.data.get("slot_list", [])
#         options = [
#             {"label": s, "value": str(i+1)}
#             for i, s in enumerate(slots)
#         ]
        
#     # Appointment Type
#     elif session and session.step == "appointment_type":
#         options = [
#             {"label": "New", "value": "new"},
#             {"label": "Follow Up", "value": "follow up"}
#         ]


#     # Treatment selection
#     elif session and session.step == "select_treatment":
#         treatments = session.data.get("treatment_list", [])
#         options = [
#             {"label": t["service_name"], "value": str(i+1)}
#             for i, t in enumerate(treatments)
#         ]

#     # --------------------------------------------
#     # FINAL RESPONSE
#     # --------------------------------------------

#     # build final response properly
#     response = {
#         "user_id": user_id,
#         "bot": reply
#     }

#     # ✅ FINAL STEP → NO INPUT FIELD
#     if session and session.step == "confirm" and message.lower() == "yes":
#         return {
#             "status": True,
#             "message": "appointment_ready",
#             "data": {
#                 "user_id": user_id,
#                 "bot": "✅ Appointment details collected successfully",
#                 "appointment_request": payload
#             }
#         }

#     # ✅ NORMAL FLOW
#     if options:
#         response["input"] = "select"
#         response["options"] = options
#     else:
#         response["input"] = "text"

#     return {
#         "status": True,
#         "message": "success",
#         "data": response
#     }




from fastapi import APIRouter, Request
from services.appointment_service import book_appointment_api
from chatbot.chatbot_flow import process_message, chat_sessions, ChatbotState
from datetime import datetime
import uuid

router = APIRouter()


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
    # 🚀 FINAL BOOKING HANDLER
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

        if session.step in ["confirm_booking", "confirm"]:
            options = [
                {"label": "Yes", "value": "yes"},
                {"label": "No", "value": "no"}
            ]

        elif session.step == "select_doctor":
            options = [
                {"label": d["emp_name"], "value": str(i+1)}
                for i, d in enumerate(session.data.get("doctor_list", []))
            ]

        elif session.step == "select_date":
            options = [
                {"label": d, "value": str(i+1)}
                for i, d in enumerate(session.data.get("date_list", []))
            ]

        elif session.step == "select_slot":
            options = [
                {"label": s, "value": str(i+1)}
                for i, s in enumerate(session.data.get("slot_list", []))
            ]

        elif session.step == "appointment_type":
            options = [
                {"label": "New", "value": "new"},
                {"label": "Follow Up", "value": "follow up"}
            ]

        elif session.step == "select_treatment":
            options = [
                {"label": t["service_name"], "value": str(i+1)}
                for i, t in enumerate(session.data.get("treatment_list", []))
            ]

    # --------------------------------------------
    # FINAL RESPONSE FORMAT
    # --------------------------------------------
    response_data = {
        "user_id": user_id,
        "bot": reply
    }

    if options:
        response_data["input"] = "select"
        response_data["options"] = options
    else:
        response_data["input"] = "text"

    return {
        "status": True,
        "message": "success",
        "data": response_data
    }