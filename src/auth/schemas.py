from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class UserRole(str, Enum):
    CUSTOMER = "customer"
    VENDOR_OWNER = "vendor_owner"
    DRIVER = "driver"

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.CUSTOMER

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    role: Optional[UserRole] = None