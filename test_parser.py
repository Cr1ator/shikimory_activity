"""Тестовый скрипт для проверки парсера Shikimori"""
import asyncio
import sys
import json
from services.shikimori_parser import parser


async def test_parser(username: str):
    """Тестирование парсера"""
    print(f"\n🔍 Тестирование парсера для пользователя: {username}\n")
    print("=" * 60)
    
    # Получаем данные профиля
    print("\n📊 Получение данных профиля...")
    data = await parser.get_profile_data(username)
    
    if not data or not data.get('success'):
        print("❌ Не удалось получить данные профиля")
        return
    
    print("✅ Данные получены успешно!\n")
    
    # Онлайн статус
    print("🟢 Онлайн статус:")
    online_status = data.get('online_status', {})
    print(f"   Статус: {online_status.get('status_text')}")
    print(f"   В сети: {'Да' if online_status.get('is_online') else 'Нет'}")
    
    # Информация о профиле
    print("\n👤 Информация о профиле:")
    profile_info = data.get('profile_info', {})
    print(f"   Имя: {profile_info.get('username')}")
    
    # Статистика аниме
    anime_stats = profile_info.get('anime_stats', {})
    if anime_stats:
        print("\n📺 Статистика аниме:")
        for stat, count in anime_stats.items():
            print(f"   {stat}")
    
    # Статистика манги
    manga_stats = profile_info.get('manga_stats', {})
    if manga_stats:
        print("\n📚 Статистика манги:")
        for stat, count in manga_stats.items():
            print(f"   {stat}")
    
    # История
    history = data.get('history', [])
    print(f"\n📝 История активности (последние {len(history)} записей):")
    for i, entry in enumerate(history[:5], 1):
        print(f"\n   {i}. {entry['anime_name']}")
        print(f"      {entry['action']}")
        print(f"      ⏰ {entry['timestamp']}")
        print(f"      🔗 {entry['anime_url']}")
    
    # Расширенная история
    print("\n\n📖 Получение расширенной истории...")
    full_history = await parser.get_history_page(username)
    
    if full_history:
        print(f"✅ Получено {len(full_history)} записей\n")
        
        print("Первые 3 записи:")
        for i, entry in enumerate(full_history[:3], 1):
            print(f"\n   {i}. {entry['anime_name']}")
            print(f"      {entry['action']}")
            print(f"      ⏰ {entry['timestamp']}")
            print(f"      ID: {entry['entry_id']}")
    else:
        print("❌ Не удалось получить расширенную историю")
    
    # Сохранение в JSON для отладки
    print("\n\n💾 Сохранение данных в test_output.json...")
    with open('test_output.json', 'w', encoding='utf-8') as f:
        json.dump({
            'profile_data': data,
            'full_history': full_history
        }, f, ensure_ascii=False, indent=2)
    print("✅ Данные сохранены")
    
    print("\n" + "=" * 60)
    print("✨ Тестирование завершено!")


async def main():
    """Главная функция"""
    if len(sys.argv) < 2:
        print("Использование: python test_parser.py <username>")
        print("Пример: python test_parser.py Bubassaka")
        sys.exit(1)
    
    username = sys.argv[1]
    await test_parser(username)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n❌ Прервано пользователем")
    except Exception as e:
        print(f"\n\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
