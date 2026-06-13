from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.deps.auth import get_current_user
from src.app.core.session import get_db_session
from src.app.crud.account import CRUDAccount
from src.app.crud.payment import CRUDPayment
from src.app.models.user import User
from src.app.schemas.account import AccountRead
from src.app.schemas.payment import PaymentRead
from src.app.schemas.user import UserProfile

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/me', response_model=UserProfile)
async def get_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.get('/me/accounts', response_model=list[AccountRead])
async def get_my_accounts(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> list[AccountRead]:
    return await CRUDAccount(session).list_by_user_id(current_user.id)


@router.get('/me/payments', response_model=list[PaymentRead])
async def get_my_payments(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> list[PaymentRead]:
    return await CRUDPayment(session).list_by_user_id(current_user.id)
