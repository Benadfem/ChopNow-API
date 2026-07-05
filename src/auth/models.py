from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

# Perfected paths matching your active PyCharm directory layout
from database import Base
from auth.schemas import UserRole


class User(Base):
    __tablename__ = "users"

    # 1. Primary Key identity column
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # 2. Core registration fields with strict constraints and optimization indexing
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # 3. Access management and user categorization columns
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # 4. System level metadata tracking
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )