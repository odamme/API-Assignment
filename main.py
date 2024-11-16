from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List
import time



app = FastAPI()

users = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    process_time = end_time - start_time
    print(f"Request: {request.method} {request.url} completed in {process_time:.2f}s")
    return response


class User(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: EmailStr
    height: float

@app.post("/register", status_code=201)
async def create_user(user: User):
    if any(person['email'] == user.email for person in users):
        raise HTTPException(
            status_code=400,
            detail="Supplied email already exists."
            )
        
    
    user_dict = user.model_dump()
    users.append(user_dict)
    return user_dict
