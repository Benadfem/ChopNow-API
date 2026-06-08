from fastapi import APIRouter, status, dependencies
from src.auth.schemas import UserCreate, UserResponse,UserLogin  # Clean relative import

# We define the router with a prefix so all routes inside automatically start with /auth
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate):
    # Simulated response matching the UserResponse schema shape
    return {
        "id": 1,
        "email": user_in.email,
        "full_name": user_in.full_name,
        "role": user_in.role,
        "is_active": True
    }





@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(credentials: UserLogin):
    # Simulated check: In Phase 3, we will verify the password hash and issue a JWT
    return {
        "access_token": "simulated_secure_jwt_token_string",
        "token_type": "bearer",
        "message": f"Successfully logged in as {credentials.email}"
    }