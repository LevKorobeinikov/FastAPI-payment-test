from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from src.app.crud.base import CRUDBase
from src.app.models.payment import Payment


class CRUDPayment(CRUDBase[Payment]):
    model = Payment

    async def list_by_user_id(self, user_id: int) -> list[Payment]:
        result = await self.session.execute(
            select(Payment)
            .where(Payment.user_id == user_id)
            .order_by(Payment.created_at.desc(), Payment.id.desc())
        )
        return list(result.scalars().all())

    async def create_unique(
        self,
        *,
        transaction_id: str,
        user_id: int,
        account_id: int,
        amount: Decimal,
    ) -> bool:
        result = await self.session.execute(
            insert(Payment)
            .values(
                transaction_id=transaction_id,
                user_id=user_id,
                account_id=account_id,
                amount=amount,
            )
            .on_conflict_do_nothing(index_elements=[Payment.transaction_id])
            .returning(Payment.id)
        )
        return result.scalar_one_or_none() is not None
