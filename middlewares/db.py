"""Middleware для работы с БД"""
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class DatabaseMiddleware(BaseMiddleware):
    """Middleware для добавления сессии БД в data"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Просто вызываем обработчик
        # БД доступна глобально через db
        return await handler(event, data)
