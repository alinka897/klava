"""
Базовый тест для функции perebor: проверка что функция вообще работает.
Либо вернет кортетж из трех элементов, либо None
"""

from structs import Layout

def test_perebor_returns_tuple_or_none():
    layout = Layout(name="test")
    
    # Слово из 2+ букв
    result = layout.perebor("Барашек")
    
    # Может быть None если буквы не найдены
    if result is not None:
        assert isinstance(result, tuple), f"Ожидался tuple, получил {type(result)}"
        assert len(result) == 3, f"Ожидалось 3 элемента, получил {len(result)}"
        print(f"✅ perebor('Барашек') вернул кортеж из {len(result)} элементов")
    else:
        print("⚠️  perebor('Барашек') вернул None (буквы не найдены в раскладке)")
