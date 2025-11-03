"""Обработчики команд start и help"""
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database import db
from keyboards import main_menu_keyboard, back_to_main_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Команда /start"""
    await state.clear()
    
    # Регистрируем пользователя
    await db.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )
    
    welcome_text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я бот для отслеживания активности на <b>Shikimori.one</b>\n\n"
        "🔔 <b>Что я умею:</b>\n"
        "• Отслеживать историю просмотров\n"
        "• Уведомлять когда пользователь в сети\n"
        "• Сообщать об изменениях в профиле\n"
        "• Гибкие настройки уведомлений\n\n"
        "Выберите действие:"
    )
    
    await message.answer(
        text=welcome_text,
        reply_markup=main_menu_keyboard(),
        parse_mode='HTML'
    )


@router.message(Command('help'))
@router.callback_query(F.data == 'help')
async def cmd_help(event: Message | CallbackQuery):
    """Команда /help"""
    help_text = (
        "📖 <b>Инструкция по использованию</b>\n\n"
        
        "<b>1. Добавление профиля</b>\n"
        "Нажмите «Добавить профиль» и отправьте никнейм пользователя Shikimori\n"
        "Пример: <code>Bubassaka</code>\n\n"
        
        "<b>2. Настройка уведомлений</b>\n"
        "В меню профиля вы можете включить/выключить:\n"
        "• 📺 История просмотров\n"
        "• 🟢 Уведомление о входе в сеть\n"
        "• ⚫ Уведомление о выходе из сети\n\n"
        
        "<b>3. Проверка статуса</b>\n"
        "Бот автоматически проверяет обновления каждые 5 минут\n"
        "Вы получите уведомление сразу после изменений\n\n"
        
        "<b>Примеры ссылок на профили:</b>\n"
        "• https://shikimori.one/Bubassaka\n"
        "• https://shikimori.one/YourNickname\n\n"
        
        "<b>Команды:</b>\n"
        "/start - Главное меню\n"
        "/help - Эта справка\n"
    )
    
    if isinstance(event, Message):
        await event.answer(
            text=help_text,
            reply_markup=back_to_main_keyboard(),
            parse_mode='HTML'
        )
    else:
        await event.message.edit_text(
            text=help_text,
            reply_markup=back_to_main_keyboard(),
            parse_mode='HTML'
        )
        await event.answer()


@router.callback_query(F.data == 'main_menu')
async def show_main_menu(callback: CallbackQuery, state: FSMContext):
    """Показать главное меню"""
    await state.clear()
    
    text = (
        "🏠 <b>Главное меню</b>\n\n"
        "Выберите действие:"
    )
    
    await callback.message.edit_text(
        text=text,
        reply_markup=main_menu_keyboard(),
        parse_mode='HTML'
    )
    await callback.answer()
