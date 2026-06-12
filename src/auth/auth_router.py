from fastapi import APIRouter, status, HTTPException
from pydantic import EmailStr

from src.auth.schemas import UserCreate, UserResponse,UserLogin  # Clean relative import
from src.db.session import get_db
from src.models.user import User
from src.auth.utils import hash_password



# We define the router with a prefix so all routes inside automatically start with /auth
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Check if the user already exists in the database
    query = select(User).where(User.email == user_in.email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists."
        )

    # 2. Hash the raw incoming password payload
    secure_hashed_password = hash_password(user_in.password)

    # 3. Instantiate the SQLAlchemy database Model
    new_user = User(
        email=user_in.email,
        hashed_password=secure_hashed_password
    )

    # 4. Save to database using async lifecycle operations
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