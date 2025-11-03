"""Вспомогательные функции"""
import re
from typing import Optional


def extract_username_from_url(text: str) -> Optional[str]:
    """
    Извлечь никнейм из URL Shikimori
    
    Args:
        text: URL или никнейм
        
    Returns:
        Никнейм пользователя или None
    """
    text = text.strip()
    
    # Если это URL
    if 'shikimori.one/' in text:
        # Паттерн для извлечения никнейма
        pattern = r'shikimori\.one/([^/\s?]+)'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    # Если это просто никнейм
    # Убираем спецсимволы
    username = re.sub(r'[^\w-]', '', text)
    
    if username and len(username) >= 2:
        return username
    
    return None


def format_timestamp(timestamp_str: str) -> str:
    """
    Форматировать временную метку
    
    Args:
        timestamp_str: Строка времени
        
    Returns:
        Отформатированная строка
    """
    # Если уже есть русский текст, возвращаем как есть
    if any(c in timestamp_str for c in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'):
        return timestamp_str
    
    # Иначе просто возвращаем
    return timestamp_str


def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Обрезать текст до максимальной длины
    
    Args:
        text: Исходный текст
        max_length: Максимальная длина
        suffix: Суффикс для обрезанного текста
        
    Returns:
        Обрезанный текст
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
