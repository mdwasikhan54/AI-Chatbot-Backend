from pydantic import BaseModel, EmailStr
from datetime import datetime

# --- User Schemas ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: EmailStr
    password: str

# --- Chat Schemas ---
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class ChatHistorySchema(BaseModel):
    message: str
    is_user_message: bool
    timestamp: datetime

    class Config:
        from_attributes = True

# --- Token Schema ---
class Token(BaseModel):
    access_token: str
    token_type: str