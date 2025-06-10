from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api.models import ComplaintCreate, ComplaintResponse, ComplaintDetail
from api.database import SessionLocal, Complaint
from api.utils import generate_complaint_id

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/complaints", response_model=ComplaintResponse)
def create_complaint(data: ComplaintCreate, db: Session = Depends(get_db)):
    complaint_id = generate_complaint_id()
    complaint = Complaint(
        complaint_id=complaint_id,
        name=data.name,
        phone_number=data.phone_number,
        email=data.email,
        complaint_details=data.complaint_details
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return {"complaint_id": complaint_id, "message": "Complaint created successfully"}

@router.get("/complaints/{complaint_id}", response_model=ComplaintDetail)
def get_complaint(complaint_id: str, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter_by(complaint_id=complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint
