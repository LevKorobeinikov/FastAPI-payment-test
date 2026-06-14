from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.models.base import BaseModel

if TYPE_CHECKING:
    from src.app.models.account import Account
    from src.app.models.user import User


class Payment(BaseModel):
    __table_args__ = (CheckConstraint('amount > 0', name='ck_payments_amount_positive'),)

    transaction_id: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        index=True,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey('accounts.id', ondelete='CASCADE'),
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    user: Mapped['User'] = relationship(back_populates='payments')
    account: Mapped['Account'] = relationship(back_populates='payments')
