from pydantic import BaseModel
from typing import Optional




###################################################
# Request Body
###################################################
class AppointmentRequest(BaseModel):
    clinic: str
    doctor: str
    patientKey: str
    appointmentType: str
    treatmentType: str
    patientName: str
    patientMobile: str
    visitReason: str
    appointmentDate: str
    selectedSlot: str
    bookedBy: Optional[str] = None
    bookingType: str
    
    
    
#######################################################
# Response Body
#######################################################
class AppointmentResponse(BaseModel):
    success: bool
    message: str
    data: dict