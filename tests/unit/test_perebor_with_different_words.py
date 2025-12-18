"""
Тест на разные русские слова не падают.
"""

from structs import Layout

def test_perebor_with_different_words():
    layout = Layout(name="test")
    
    test_words = ["мама", "папа", "кошка", "собака", "дом"]
    
    for word in test_words:
        try:
            result = layout.perebor(word)
            if result is not None:
                convs, _, _ = result
                print(f"✅ '{word}': convs={convs}")
            else:
                print(f"⚠️  '{word}': None (символы не найдены)")
        except Exception as e:
            print(f"❌ '{word}': упало с ошибкой {e}")
            raise
    
    print("✅ Все слова обработались без падений")
