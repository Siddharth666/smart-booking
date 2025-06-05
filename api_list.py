# from fastapi import APIRouter, Depends, HTTPException
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import FastAPI, HTTPException
# from models.users import UserCreate
# from fastapi import Depends, Form, Request
# from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
# from bson import ObjectId
# from datetime import datetime
# from auth import get_current_user  # Adjust path
# from database import db

# app = FastAPI()
# router = APIRouter()

# # Login and Authentication APIs
# @app.post("/register")
# @app.post("/login")

# #Bookings API
# @router.post("/bookings/confirm")
# @app.get("/admin/bookings")
# @router.post("/create-payment-intent")

# #Service APIs
# @router.get("/services")
# @router.get("/services/{service_id}")