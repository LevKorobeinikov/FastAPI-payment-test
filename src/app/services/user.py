from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.security import get_password_hash, verify_password
from src.app.crud.user import CRUDUser
from src.app.models.user import User
from src.app.services.exceptions import EmailAlreadyExistsError


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = CRUDUser(session)

    @staticmethod
    def _normalize_email(email: str) -> str:
        return email.strip().lower()

    async def authenticate(self, email: str, password: str) -> User | None:
        user = await self.repo.get_by_email(self._normalize_email(email))
        if user is None or not verify_password(password, user.hashed_password):
            return None
        return user

    async def create_user(
        self,
        *,
        email: str,
        full_name: str,
        password: str,
        is_admin: bool = False,
    ) -> User:
        normalized_email = self._normalize_email(email)
        if await self.repo.get_by_email(normalized_email) is not None:
            raise EmailAlreadyExistsError()
        user = await self.repo.create(
            email=normalized_email,
            full_name=full_name.strip(),
            hashed_password=get_password_hash(password),
            is_admin=is_admin,
        )
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_user(
        self,
        user: User,
        *,
        email: str | None = None,
        full_name: str | None = None,
        password: str | None = None,
        is_admin: bool | None = None,
        is_active: bool | None = None,
    ) -> User:
        if email is not None:
            normalized_email = self._normalize_email(email)
            existing = await self.repo.get_by_email(normalized_email)
            if existing is not None and existing.id != user.id:
                raise EmailAlreadyExistsError()
            user.email = normalized_email
        if full_name is not None:
            user.full_name = full_name.strip()
        if password is not None:
            user.hashed_password = get_password_hash(password)
        if is_admin is not None:
            user.is_admin = is_admin
        if is_active is not None:
            user.is_active = is_active
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user: User) -> None:
        await self.repo.delete(user)
        await self.session.commit()
