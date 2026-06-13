from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.deps.auth import require_admin
from src.app.core.session import get_db_session
from src.app.models.user import User
from src.app.schemas.user import (
    AdminRead,
    UserCreate,
    UserProfile,
    UserUpdate,
)
from src.app.services.exceptions import (
    EmailAlreadyExistsError,
    UserNotFoundError,
)
from src.app.services.user import UserService

router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(require_admin)],
)


@router.get('/me', response_model=UserProfile)
async def get_admin_me(
    current_admin: User = Depends(require_admin),
) -> User:
    return current_admin


@router.get('/users', response_model=list[AdminRead])
async def list_users(
    session: AsyncSession = Depends(get_db_session),
) -> list[User]:
    return await UserService(session).list_users()


@router.post(
    '/users',
    response_model=AdminRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    payload: UserCreate,
    session: AsyncSession = Depends(get_db_session),
) -> User:
    try:
        return await UserService(session).create_user(
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


@router.patch(
    '/users/{user_id}',
    response_model=AdminRead,
)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> User:
    try:
        return await UserService(session).update_user(
            user_id=user_id,
            email=str(payload.email) if payload.email is not None else None,
            full_name=payload.full_name,
            password=payload.password,
            is_admin=payload.is_admin,
            is_active=payload.is_active,
        )
    except UserNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from None
    except EmailAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from None


@router.delete(
    '/users/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_admin: User = Depends(require_admin),
) -> Response:
    if current_admin.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot delete yourself',
        )
    try:
        await UserService(session).delete_user(user_id)
    except UserNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from None
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
