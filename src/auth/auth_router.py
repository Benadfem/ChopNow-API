from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Clean async dependency layer
from src.db.session import get_db

from src.auth.schemas import UserCreate, UserResponse, UserLogin
from src.auth.models import User
from src.auth.utils import hash_password



users = []
#

# We define the router with a prefix so all routes inside automatically start with /auth
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Query using select() and referencing 'user_data'
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists."
        )

    # 2. Hash password referencing 'user_data'
    secure_hashed_password = hash_password(user_data.password)

    # 3. Instantiate model referencing 'user_data'
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=secure_hashed_password,
        role=user_data.role
    )

    # 4. Async commit lifecycle
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

#It is time to write the code to display the users that has been registered
@router.get("/")
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

#to update the user profile
from src.auth.schemas import UserUpdate


@router.patch("/users/{email}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(email: EmailStr, user_update: UserUpdate):
    for user in users:
        if user["email"] == email:
            # Only update fields that were actually provided in the request body
            if user_update.full_name is not None:
                user["full_name"] = user_update.full_name
            if user_update.role is not None:
                user["role"] = user_update.role
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found for update 😒"
    )


#for user delete endpoint
@router.delete("/users/{email}", status_code=status.HTTP_200_OK)
async def deactivate_user(email: EmailStr):
    for user in users:
        if user["email"] == email:
            if not user["is_active"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Account is already deactivated! 🛑"
                )
            user["is_active"] = False
            return {
                "message": f"User account associated with {email} has been successfully deactivated."
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found for deactivation 😒"
    )