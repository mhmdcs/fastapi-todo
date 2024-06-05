from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    email: EmailStr
    password: str

class TaskBase(BaseModel):
    title: str
    content: str
    done: bool = False

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    created_at: datetime
    id: int
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class TaskStatus(BaseModel):
    done: bool = False

class TaskShare(BaseModel):
    email: EmailStr
    share: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None