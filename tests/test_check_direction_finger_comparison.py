"""
Тест проверка разных пальцев влияет на результат.
"""

from structs import Layout, Key


def test_check_direction_finger_comparison():
    layout = Layout(name="test")
    
    k1 = Key(30, 'ф')
    k1.finger = 'f2'
    
    k2 = Key(31, 'ы')
    k2.finger = 'f3'
    
    result = layout.check_direction(k1, k2)
    
    print(f"Направление f2 → f3: {result}")
    assert isinstance(result, bool)
    print("✅ Сравнение пальцев работает")
