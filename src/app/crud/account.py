from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from src.app.crud.base import CRUDBase
from src.app.models.account import Account


class CRUDAccount(CRUDBase[Account]):
    model = Account

    async def list_by_user_id(self, user_id: int) -> list[Account]:
        result = await self.session.execute(
            select(Account).where(Account.user_id == user_id).order_by(Account.id.asc())
        )
        return list(result.scalars().all())

    async def create_with_id(self, *, account_id: int, user_id: int) -> Account:
        result = await self.session.execute(
            insert(Account)
            .values(id=account_id, user_id=user_id)
            .on_conflict_do_nothing(index_elements=[Account.id])
            .returning(Account)
        )
        account = result.scalar_one_or_none()
        if account is not None:
            return account

        existing = await self.get_by_id(account_id)
        if existing is None:
            msg = f'Account {account_id} was not created and does not exist'
            raise RuntimeError(msg)
        return existing

    async def add_balance(self, account: Account, amount: Decimal) -> Account:
        account.balance += amount
        await self.session.flush()
        return account
