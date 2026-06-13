from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.app.core.base import Base

if TYPE_CHECKING:
    from src.app.models.account import Account
    from src.app.models.user import User


class Payment(Base):
    __table_args__ = (CheckConstraint('amount > 0', name='ck_payments_amount_positive'),)
    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        index=True,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey('accounts.id', ondelete='CASCADE'),
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    user: Mapped['User'] = relationship(back_populates='payments')
    account: Mapped['Account'] = relationship(back_populates='payments')
