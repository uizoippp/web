from pydantic import BaseModel

# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"


# ===== User schemas =====
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str]
    phone_number: Optional[str]
    role: Optional[RoleEnum] = "user"
    is_active: Optional[int] = 1


class UserCreate(UserBase):
    hashed_password: str

class UserLogin(UserBase):
    id: int
    hashed_password: str
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ===== Session schemas =====
class SessionBase(BaseModel):
    is_active: Optional[int] = 1


class SessionOut(SessionBase):
    id: int
    user_id: int
    created_at: Optional[datetime]
    last_active_at: Optional[datetime]

    class Config:
        from_attributes = True


# ===== DeviceInfo schemas =====
class DeviceInfoBase(BaseModel):
    device_fingerprint: Optional[str]
    ip_address: Optional[str]
    last_seen: Optional[datetime]


class DeviceInfoOut(DeviceInfoBase):
    id: int
    first_seen: Optional[datetime]

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    id: int
    token: str
    token_type: str = "bearer"