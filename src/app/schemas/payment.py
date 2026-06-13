from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from pydantic import Field

from src.app.schemas.base import BaseReadSchema, BaseSchema


class PaymentWebhookStatus(StrEnum):
    PROCESSED = 'processed'
    IGNORED = 'ignored'


class PaymentRead(BaseReadSchema):
    transaction_id: UUID
    user_id: int
    account_id: int
    amount: Decimal
    created_at: datetime


class PaymentWebhookRequest(BaseSchema):
    transaction_id: UUID
    user_id: int
    account_id: int
    amount: Decimal = Field(gt=0)
    signature: str = Field(min_length=64, max_length=64)


class PaymentWebhookResponse(BaseSchema):
    status: PaymentWebhookStatus
    user_id: int
    account_id: int
    balance: Decimal
