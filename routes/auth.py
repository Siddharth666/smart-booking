from fastapi import FastAPI, HTTPException
from pydantic import EmailStr
from models.users import UserCreate
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext

app = FastAPI()
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["smartbooking"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# @app.post("/register")
# async def register_user(user: UserCreate):
#     existing_user = await db.users.find_one({"email": user.email})
#     if existing_user:
#         raise HTTPException(status_code=400, detail="User already exists")

#     hashed_pw = pwd_context.hash(user.password)
#     user_data = user.dict()
#     user_data["password"] = hashed_pw

#     result = await db.users.insert_one(user_data)
#     return {"message": "User registered successfully", "id": str(result.inserted_id)}
