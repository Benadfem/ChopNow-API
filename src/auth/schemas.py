from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

# 1. Definitive User Actors mapping to Lagos food-tech marketplace domains
class UserRole(str, Enum):
    CUSTOMER = "customer"
    VENDOR_OWNER = "vendor_owner"
    DRIVER = "driver"

# 2. Strict Payload validation for User Registration transactions
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100, description="User legal profile identity name")
    password: str = Field(..., min_length=8, description="Cryptographic registration credential baseline")
    role: UserRole = UserRole.CUSTOMER

# 3. Clean Outbound JSON formatter (Saves bandwidth, drops password hash leak vectors)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool

    # Corrected Pydantic V2 metadata configuration object declaration
    model_config = ConfigDict(from_attributes=True)

# 4. Lean, specialized schema optimized strictly for login credential checks
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

# 5. Safe Profile Management schema preventing explicit role-escalation exploits
class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)