from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.models.base import BaseModel

if TYPE_CHECKING:
    from src.app.models.payment import Payment
    from src.app.models.user import User


class Account(BaseModel):
    __table_args__ = (CheckConstraint('balance >= 0', name='ck_accounts_balance_non_negative'),)

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        index=True,
    )
    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), server_default='0')
    user: Mapped['User'] = relationship(back_populates='accounts')
    payments: Mapped[list['Payment']] = relationship(back_populates='account')
