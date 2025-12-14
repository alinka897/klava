"""
Тест на одинаковые клавиши возвращает True.
"""

from structs import Layout, Key


def test_check_direction_same_key_returns_true():
    
    layout = Layout(name="test")
    
    # Одна и та же клавиша
    k1 = Key(30, 'ф')
    k2 = Key(30, 'ф')
    
    result = layout.check_direction(k1, k2)
    
    assert result is True, f"Ожидалось True, получил {result}"
    print("✅ Одинаковые клавиши → True")
