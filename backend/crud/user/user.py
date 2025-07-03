from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Users, Sessions, DeviceInfo
from crud.user.models import UserCreate, UserLogin, DeviceInfoOut, TokenResponse
from db.db import get_session
from auth.auth import generate_token

router = APIRouter()

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, device: DeviceInfoOut, session: AsyncSession = Depends(get_session)):
    # Tạo user
    user = Users(**user_data.dict())
    session.add(user)

    # Commit lần 1 để lấy user.id
    try:
        await session.commit()
        await session.refresh(user)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user")

    # Tạo device info
    device_info = DeviceInfo(
        user_id=user.id,
        device_fingerprint=device.device_fingerprint,
        ip_address=device.ip_address,
        last_seen=device.last_seen
    )
    session.add(device_info)

    # Commit lần 2
    try:
        await session.commit()
        await session.refresh(device_info)
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to create session/device")

    # Tạo session
    user_session = Sessions(user_id=user.id, device_id=device_info.id, is_active=True)
    session.add(user_session)
    try:
        await session.commit()
        await session.refresh(user_session)
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to create session")

    # Sinh token
    try:
        token = generate_token(user.id)
    except Exception:
        raise HTTPException(status_code=500, detail="Error generating token")

    return TokenResponse(id=user.id, token=token)

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(data: UserLogin, device: DeviceInfoOut, session: AsyncSession = Depends(get_session)):
    try: 
        result = await session.execute(
            select(Users).where(Users.username == data.username)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="No any accounts found!")
    
    user = result.scalar_one_or_none()
    if not user or user.hashed_password != data.hashed_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")

    # Có tài khoản và mật khẩu đúng, kiểm tra device
    is_old_device = await session.scalar(
        select(DeviceInfo).where(
            DeviceInfo.user_id == user.id,
            DeviceInfo.device_fingerprint == device.device_fingerprint,
            DeviceInfo.ip_address == device.ip_address
        )
    )
    
    if not is_old_device:
        # Tạo mới device info
        device_info = DeviceInfo(
            user_id=user.id,
            device_fingerprint=device.device_fingerprint,
            ip_address=device.ip_address,
            last_seen=device.last_seen
        )
        session.add(device_info)
        try:
            await session.commit()
            await session.refresh(device_info)
        except Exception:
            await session.rollback()
            raise HTTPException(status_code=500, detail="Failed to create device info")
        
        # Tạo session mới
        user_session = Sessions(user_id=user.id, device_id=device_info.id, is_active=True)
        session.add(user_session)
        try:
            await session.commit()
            await session.refresh(user_session)
        except Exception:
            await session.rollback()
            raise HTTPException(status_code=500, detail="Failed to create session")
        
    else:
        # Cập nhật device info
        is_old_device.last_seen = device.last_seen
        is_old_device.ip_address = device.ip_address
        try:
            await session.commit()
            await session.refresh(is_old_device)
        except Exception:
            await session.rollback()
            raise HTTPException(status_code=500, detail="Failed to update device info")
    
    token = generate_token(user.id)
    return TokenResponse(id=user.id, token=token)