from pydantic import BaseModel, EmailStr, constr
from datetime import datetime

class ComplaintCreate(BaseModel):
    name: str
    phone_number: constr(min_length=10, max_length=15)
    email: EmailStr
    complaint_details: str

class ComplaintResponse(BaseModel):
    complaint_id: str
    message: str

class ComplaintDetail(BaseModel):
    complaint_id: str
    name: str
    phone_number: str
    email: str
    complaint_details: str
    created_at: datetime
