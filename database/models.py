"""Модели базы данных"""
from datetime import datetime
from sqlalchemy import BigInteger, String, Boolean, DateTime, Integer, Text, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional


class Base(DeclarativeBase):
    pass


class User(Base):
    """Модель пользователя Telegram"""
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class TrackedProfile(Base):
    """Отслеживаемые профили Shikimori"""
    __tablename__ = 'tracked_profiles'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    shikimori_username: Mapped[str] = mapped_column(
        String(255), nullable=False)
    shikimori_user_id: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True)  # ID пользователя на Shikimori (постоянный)

    # Настройки уведомлений
    notify_history: Mapped[bool] = mapped_column(Boolean, default=True)
    notify_online: Mapped[bool] = mapped_column(Boolean, default=False)
    notify_offline: Mapped[bool] = mapped_column(Boolean, default=False)
    notify_achievements: Mapped[bool] = mapped_column(Boolean, default=False)

    # Статус
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now)

    # Последние данные
    last_online_status: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True)
    last_history_entry: Mapped[Optional[str]
                               ] = mapped_column(Text, nullable=True)
    was_online: Mapped[bool] = mapped_column(Boolean, default=False)


class HistoryEntry(Base):
    """История активности на Shikimori"""
    __tablename__ = 'history_entries'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(Integer, nullable=False)
    entry_id: Mapped[str] = mapped_column(
        String(50), nullable=False)  # ID записи на Shikimori

    # Данные записи
    anime_name: Mapped[str] = mapped_column(String(500), nullable=False)
    anime_url: Mapped[str] = mapped_column(String(500), nullable=False)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now)
    notified: Mapped[bool] = mapped_column(Boolean, default=False)


class OnlineStatus(Base):
    """История онлайн-статуса"""
    __tablename__ = 'online_status'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_online: Mapped[bool] = mapped_column(Boolean, nullable=False)
    status_text: Mapped[str] = mapped_column(String(255), nullable=False)
    checked_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now)
