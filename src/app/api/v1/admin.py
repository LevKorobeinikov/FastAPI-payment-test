from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.deps.auth import require_admin
from src.app.api.deps.db import get_session
from src.app.crud.user import CRUDUser
from src.app.models.user import User
from src.app.schemas.user import AdminRead, UserCreate, UserProfile, UserUpdate
from src.app.services.exceptions import EmailAlreadyExistsError
from src.app.services.user import UserService

router = APIRouter(prefix='/admin', tags=['admin'])


async def _get_user_with_accounts_or_404(
    repo: CRUDUser,
    user_id: int,
) -> User:
    user = await repo.get_by_id_with_accounts(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )
    return user


@router.get('/me', response_model=UserProfile)
async def get_admin_me(current_admin: User = Depends(require_admin)) -> User:
    return current_admin


@router.get('/users', response_model=list[AdminRead])
async def list_users(
    session: AsyncSession = Depends(get_session),
    _: User = Depends(require_admin),
) -> list[User]:
    return await CRUDUser(session).list_with_accounts()


@router.post('/users', response_model=AdminRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(require_admin),
) -> User:
    try:
        user = await UserService(session).create_user(
            email=str(payload.email),
            full_name=payload.full_name,
            password=payload.password,
            is_admin=payload.is_admin,
        )
    except EmailAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from None
    return await _get_user_with_accounts_or_404(CRUDUser(session), user.id)


@router.patch('/users/{user_id}', response_model=AdminRead)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(require_admin),
) -> User:
    repo = CRUDUser(session)
    user = await repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    try:
        updated = await UserService(session).update_user(
            user=user,
            email=str(payload.email) if payload.email is not None else None,
            full_name=payload.full_name,
            password=payload.password,
            is_admin=payload.is_admin,
            is_active=payload.is_active,
        )
    except EmailAlreadyExistsError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from None
    return await _get_user_with_accounts_or_404(repo, updated.id)


@router.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(require_admin),
) -> Response:
    if current_admin.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Cannot delete yourself'
        )
    user = await CRUDUser(session).get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    await UserService(session).delete_user(user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
