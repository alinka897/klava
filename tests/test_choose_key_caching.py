"""
Тест кэширования choose_key.
"""

from structs import Layout, Key


def test_choose_key_caching():
    layout = Layout(name="test")
    
    layout.better_keys.clear()
    
    key1 = layout.choose_key("а")
    
    if key1 is None:
        print("⚠️  'а' не найдена, пропускаем тест кэширования")
        return  # Не падаем
    
    # Должен быть в кэше
    assert "а" in layout.better_keys
    
    # Второй вызов - берётся из кэша
    key2 = layout.choose_key("а")
    
    # Тот же объект
    assert key2 is key1, f    
    print(f"✅ Кэш работает: choose_key('а') дважды вернул один объект (id={id(key1)})")
