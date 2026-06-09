from fastapi import APIRouter, status, HTTPException
from pydantic import EmailStr

from src.auth.schemas import UserCreate, UserResponse,UserLogin  # Clean relative import

# We define the router with a prefix so all routes inside automatically start with /auth
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

#let's create a demo lists of users
users = []

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate):
    # Simulated response matching the UserResponse schema shape
    response = {
        "id": len(users) + 1,
        "email": user_in.email,
        "full_name": user_in.full_name,
        "role": user_in.role,
        "is_active": True
    }

    users.append(response)
    return response

#It is time to write the code to display the users that has been registered
@router.get("/users")
async def get_users():
    return users
#let's try to fetch user according to email_address.
@router.get("/users/{email}",response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(email: EmailStr):
    for user in users:
        if user["email"] == email:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found😒")

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(credentials: UserLogin):
    # Simulated check: In Phase 3, we will verify the password hash and issue a JWT
    return {
        "access_token": "simulated_secure_jwt_token_string",
        "token_type": "bearer",
        "message": f"Successfully logged in as {credentials.email}"
    }