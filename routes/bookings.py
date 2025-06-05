from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime
from auth import get_current_user  # Adjust path
from database import db

router = APIRouter()

class BookingConfirmRequest(BaseModel):
    booking_id: str
    payment_intent: str = None

@router.post("/bookings/confirm")
async def confirm_booking(
    req: BookingConfirmRequest,
    user=Depends(get_current_user)
):
    booking = await db.bookings.find_one({"_id": ObjectId(req.booking_id)})

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking["user_email"] != user["email"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    await db.bookings.update_one(
        {"_id": ObjectId(req.booking_id)},
        {
            "$set": {
                "paid": True,
                "payment_intent": req.payment_intent,
                "paid_at": datetime.utcnow()
            }
        }
    )
    return {"message": "Booking confirmed"}
