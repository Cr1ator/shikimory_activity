"""Handlers package"""
from aiogram import Router
from handlers import start, profile, settings


def setup_routers() -> Router:
    """Настроить все роутеры"""
    router = Router()
    
    router.include_router(start.router)
    router.include_router(profile.router)
    router.include_router(settings.router)
    
    return router


__all__ = ['setup_routers']
