"""
Тест для функции на возврат true или false
"""

from structs import Layout, Key


def test_check_direction_returns_bool():
    
    layout = Layout(name="test")
    
    # Создаем две разные клавиши
    k1 = Key(30, 'ф')
    k2 = Key(31, 'ы')
    
    result = layout.check_direction(k1, k2)
    
    assert isinstance(result, bool), f"Ожидался bool, получил {type(result)}"
    print(f"✅ check_direction возвращает bool: {result}")
