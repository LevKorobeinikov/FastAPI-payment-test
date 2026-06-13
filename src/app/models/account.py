from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.app.core.base import Base

if TYPE_CHECKING:
    from src.app.models.payment import Payment
    from src.app.models.user import User


class Account(Base):
    __table_args__ = (CheckConstraint('balance >= 0', name='ck_accounts_balance_non_negative'),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        index=True,
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        server_default='0',
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    user: Mapped['User'] = relationship(back_populates='accounts')
    payments: Mapped[list['Payment']] = relationship(back_populates='account')
