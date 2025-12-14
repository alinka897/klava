"""
Тест для функции одинаковые слова = одинаковые результаты.
"""

from structs import Layout


def test_perebor_consistent_results():
    layout = Layout(name="test")
    
    word = "программа"
    result1 = layout.perebor(word)
    result2 = layout.perebor(word)
    
    # Оба должны быть None или оба не None
    assert (result1 is None) == (result2 is None)
    
    if result1 is not None and result2 is not None:
        assert result1 == result2, f"Результаты разные: {result1} != {result2}"
        print("✅ Результаты консистентны")
    else:
        print(f"⚠️  Слово '{word}' не обработалось (вернуло None)")
