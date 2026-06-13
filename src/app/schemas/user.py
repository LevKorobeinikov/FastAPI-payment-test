from pydantic import BaseModel, ConfigDict, EmailStr

from src.app.schemas.account import AccountRead


class UserProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    full_name: str


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    is_admin: bool = False


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = None
    is_admin: bool | None = None
    is_active: bool | None = None


class AdminRead(UserProfile):
    is_admin: bool
    is_active: bool
    accounts: list[AccountRead]
