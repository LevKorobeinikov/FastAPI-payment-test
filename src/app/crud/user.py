from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.app.crud.base import CRUDBase
from src.app.models.user import User


class CRUDUser(CRUDBase[User]):
    model = User

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id_with_accounts(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(User).options(selectinload(User.accounts)).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def list_with_accounts(self) -> list[User]:
        result = await self.session.execute(
            select(User).options(selectinload(User.accounts)).order_by(User.id.asc())
        )
        return list(result.scalars().all())

    async def create(
        self,
        *,
        email: str,
        full_name: str,
        hashed_password: str,
        is_admin: bool = False,
        is_active: bool = True,
    ) -> User:
        user = User(
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
            is_admin=is_admin,
            is_active=is_active,
        )
        self.session.add(user)
        await self.session.flush()
        return user

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
