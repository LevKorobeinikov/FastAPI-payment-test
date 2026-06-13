from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.config import settings
from src.app.core.session import get_db_session
from src.app.crud.user import CRUDUser
from src.app.models.user import User
from src.app.schemas.token import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f'{settings.api_v1_prefix}/auth/login',
)

_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


def _decode_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return int(TokenPayload(**payload).sub)
    except (JWTError, ValidationError, ValueError):
        raise _CREDENTIALS_EXCEPTION from None


async def get_current_user(
    session: AsyncSession = Depends(get_db_session),
    token: str = Depends(oauth2_scheme),
) -> User:
    user_id = _decode_token(token)
    user = await CRUDUser(session).get_by_id(user_id)
    if user is None or not user.is_active:
        raise _CREDENTIALS_EXCEPTION
    return user


async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Admin permissions required',
        )
    return current_user
