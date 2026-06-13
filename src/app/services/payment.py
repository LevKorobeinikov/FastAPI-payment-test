import hmac
from decimal import Decimal
from hashlib import sha256

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.config import settings
from src.app.crud.account import CRUDAccount
from src.app.crud.payment import CRUDPayment
from src.app.crud.user import CRUDUser
from src.app.schemas.payment import PaymentWebhookRequest
from src.app.services.exceptions import (
    AccountOwnershipError,
    InvalidPaymentSignatureError,
    UserNotFoundError,
)


class PaymentService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = CRUDUser(session)
        self.account_repo = CRUDAccount(session)
        self.payment_repo = CRUDPayment(session)

    @staticmethod
    def _amount_to_str(amount: Decimal) -> str:
        normalized = amount.normalize()
        if normalized == normalized.to_integral():
            return str(
                normalized.quantize(
                    Decimal('1'),
                ),
            )
        return (
            format(
                normalized,
                'f',
            )
            .rstrip('0')
            .rstrip('.')
        )

    @staticmethod
    def make_signature(
        payload: PaymentWebhookRequest,
    ) -> str:
        return sha256(
            f'{payload.account_id}'
            f'{PaymentService._amount_to_str(payload.amount)}'
            f'{payload.transaction_id}'
            f'{payload.user_id}'
            f'{settings.payment_secret_key}'.encode()
        ).hexdigest()

    @staticmethod
    def verify_signature(
        payload: PaymentWebhookRequest,
    ) -> bool:
        return hmac.compare_digest(
            PaymentService.make_signature(payload),
            payload.signature,
        )

    async def process_webhook(
        self,
        payload: PaymentWebhookRequest,
    ) -> tuple[bool, Decimal]:
        if not self.verify_signature(payload):
            raise InvalidPaymentSignatureError()
        async with self.session.begin():
            user = await self.user_repo.get_by_id(
                payload.user_id,
            )
            if user is None:
                raise UserNotFoundError()
            account = await self.account_repo.get_by_id(
                payload.account_id,
            )
            if account is None:
                account = await self.account_repo.create_with_id(
                    account_id=payload.account_id,
                    user_id=payload.user_id,
                )
            if account.user_id != payload.user_id:
                raise AccountOwnershipError()
            is_new = await self.payment_repo.create_unique(
                transaction_id=str(
                    payload.transaction_id,
                ),
                user_id=payload.user_id,
                account_id=payload.account_id,
                amount=payload.amount,
            )
            if not is_new:
                return False, account.balance
            updated_account = await self.account_repo.add_balance(
                account,
                payload.amount,
            )
            return True, updated_account.balance
