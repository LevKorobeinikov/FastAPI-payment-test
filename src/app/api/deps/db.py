from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.session import get_db_session


def get_session(session: AsyncSession = Depends(get_db_session)) -> AsyncSession:
    return session
