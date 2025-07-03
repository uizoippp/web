from typing import List, Optional

from sqlalchemy import DateTime, Enum, ForeignKeyConstraint, Index, Integer, String, Text, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        Index('email', 'email', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(256))
    full_name: Mapped[Optional[str]] = mapped_column(String(50))
    phone_number: Mapped[Optional[str]] = mapped_column(String(10))
    is_active: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'1'"))
    role: Mapped[Optional[str]] = mapped_column(Enum('user', 'admin'), server_default=text("'user'"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    device_info: Mapped[List['DeviceInfo']] = relationship('DeviceInfo', back_populates='user')
    sessions: Mapped[List['Sessions']] = relationship('Sessions', back_populates='user')


class DeviceInfo(Base):
    __tablename__ = 'device_info'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='device_info_ibfk_1'),
        Index('user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    device_fingerprint: Mapped[Optional[str]] = mapped_column(Text)
    first_seen: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    last_seen: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))

    user: Mapped['Users'] = relationship('Users', back_populates='device_info')
    sessions: Mapped[List['Sessions']] = relationship('Sessions', back_populates='device')


class Sessions(Base):
    __tablename__ = 'sessions'
    __table_args__ = (
        ForeignKeyConstraint(['device_id'], ['device_info.id'], ondelete='CASCADE', name='sessions_ibfk_2'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='sessions_ibfk_1'),
        Index('device_id', 'device_id'),
        Index('user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    device_id: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'1'"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    last_active_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    device: Mapped['DeviceInfo'] = relationship('DeviceInfo', back_populates='sessions')
    user: Mapped['Users'] = relationship('Users', back_populates='sessions')
