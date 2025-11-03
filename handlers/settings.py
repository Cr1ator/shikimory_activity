"""Обработчики настроек"""
from aiogram import Router, F
from aiogram.types import CallbackQuery

from database import db
from keyboards import settings_keyboard

router = Router()


@router.callback_query(F.data.startswith('settings:'))
async def show_settings(callback: CallbackQuery):
    """Показать настройки профиля"""
    profile_id = int(callback.data.split(':')[1])
    
    # Получаем профиль
    profiles = await db.get_user_profiles(callback.from_user.id)
    profile = next((p for p in profiles if p.id == profile_id), None)
    
    if not profile:
        await callback.answer("❌ Профиль не найден", show_alert=True)
        return
    
    text = (
        f"⚙️ <b>Настройки уведомлений</b>\n\n"
        f"Профиль: <b>{profile.shikimori_username}</b>\n\n"
        "Нажмите на пункт, чтобы включить/выключить уведомления:"
    )
    
    await callback.message.edit_text(
        text=text,
        reply_markup=settings_keyboard(profile),
        parse_mode='HTML'
    )
    await callback.answer()


@router.callback_query(F.data.startswith('toggle:'))
async def toggle_setting(callback: CallbackQuery):
    """Переключить настройку"""
    parts = callback.data.split(':')
    setting_name = parts[1]
    profile_id = int(parts[2])
    
    # Получаем профиль
    profiles = await db.get_user_profiles(callback.from_user.id)
    profile = next((p for p in profiles if p.id == profile_id), None)
    
    if not profile:
        await callback.answer("❌ Профиль не найден", show_alert=True)
        return
    
    # Переключаем настройку
    setting_key = f"notify_{setting_name}"
    current_value = getattr(profile, setting_key, False)
    new_value = not current_value
    
    # Сохраняем в БД
    await db.update_profile_settings(
        profile_id,
        {setting_key: new_value}
    )
    
    # Обновляем локальный объект
    setattr(profile, setting_key, new_value)
    
    # Названия настроек для сообщения
    setting_names = {
        'history': 'История просмотров',
        'online': 'Пользователь в сети',
        'offline': 'Пользователь вышел',
        'achievements': 'Достижения'
    }
    
    status = "включены" if new_value else "выключены"
    setting_title = setting_names.get(setting_name, setting_name)
    
    # Обновляем сообщение
    text = (
        f"⚙️ <b>Настройки уведомлений</b>\n\n"
        f"Профиль: <b>{profile.shikimori_username}</b>\n\n"
        "Нажмите на пункт, чтобы включить/выключить уведомления:"
    )
    
    await callback.message.edit_text(
        text=text,
        reply_markup=settings_keyboard(profile),
        parse_mode='HTML'
    )
    
    await callback.answer(
        f"✅ {setting_title}: {status}",
        show_alert=False
    )
