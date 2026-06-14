from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.models.base import BaseModel

if TYPE_CHECKING:
    from src.app.models.account import Account
    from src.app.models.payment import Payment


class User(BaseModel):
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(server_default='false')
    is_active: Mapped[bool] = mapped_column(server_default='true')
    accounts: Mapped[list['Account']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )
    payments: Mapped[list['Payment']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )
