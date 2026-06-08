from fastapi import APIRouter, status
from src.auth.schemas import UserCreate, UserResponse  # Clean relative import

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