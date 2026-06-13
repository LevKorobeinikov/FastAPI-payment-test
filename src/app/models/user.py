from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.app.core.base import Base

if TYPE_CHECKING:
    from src.app.models.account import Account
    from src.app.models.payment import Payment


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(server_default='false')
    is_active: Mapped[bool] = mapped_column(server_default='true')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    accounts: Mapped[list['Account']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )
    payments: Mapped[list['Payment']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )
