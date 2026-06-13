from decimal import Decimal

from src.app.schemas.base import BaseReadSchema


class AccountRead(BaseReadSchema):
    user_id: int
    balance: Decimal
