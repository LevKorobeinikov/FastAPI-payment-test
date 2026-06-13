from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.session import get_db_session
from src.app.schemas.token import Token
from src.app.services.user import UserService

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db_session),
) -> Token:
    token = await UserService(session).login(
        email=form_data.username,
        password=form_data.password,
    )
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return token
