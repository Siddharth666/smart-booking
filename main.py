from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from models.users import UserCreate
from fastapi import Depends, Form, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from database import db
from passlib.context import CryptContext
from jose import JWTError, jwt
from auth.jwt_handler import create_access_token
from routes.services import router as services_router
from routes import payments
from pydantic import BaseModel
from typing import Optional



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/register")
async def register_user(user: UserCreate):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = pwd_context.hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_pw
    print("User entered password:", user.password)
    result = await db.users.insert_one(user_data)
    return {"message": "User registered successfully", "id": str(result.inserted_id)}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    #print("Stored hashed password:", user["password"])
    user = await db.users.find_one({"email": form_data.username})
    print(user)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    print("Password valid:", pwd_context.verify(form_data.password, user["password"]))
    if not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {
        "sub": user["email"],
        "role": user.get("role", "customer")
    }

    #token = create_access_token(data={"sub": user["email"]})

    token = create_access_token(data=token_data)

    #return {"access_token": token, "token_type": "bearer", "user": {"name": user["name"], "email": user["email"]}}
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "email": user["email"],
            "name": user["name"],
            "role": user.get("role", "customer")
        }
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "my-super-secret"
ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        role = payload.get("role")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"email": email, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/bookings")
async def get_bookings(current_user: str = Depends(get_current_user)):
    # Dummy response - later connect to real MongoDB booking data
    return [
        {"id": 1, "name": "Hotel A", "user": current_user},
        {"id": 2, "name": "Hotel B", "user": current_user},
    ]

@app.get("/admin/bookings")
async def get_all_bookings(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    bookings = await db.bookings.find().to_list(length=100)
    return bookings

app.include_router(services_router) 

app.include_router(payments.router, prefix="/api")

class BookingSchema(BaseModel):
    service_id: str
    day: str  # Or use `datetime.date` if it's a date
    time: str  # Or use `datetime.time` if it's a time
    plan: Optional[str] = None
    price: float

# @app.post("/bookings")
# async def create_booking(booking: BookingSchema, user: User = Depends(get_current_user)):
#     """
#     Create a booking in MongoDB
#     """
#     booking_doc = {
#         "service_id": booking.service_id,
#         "day": booking.day,
#         "time": booking.time,
#         "plan": booking.plan,
#         "price": booking.price,
#         "user_id": user.id,
#         "user_email": user.email,
#         "paid": False,
#         "created_at": datetime.utcnow()
#     }
#     result = await db.bookings.insert_one(booking_doc)
#     return {"message": "Booking created", "booking_id": str(result.inserted_id)}
