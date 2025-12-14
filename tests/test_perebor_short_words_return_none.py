"""
Тест для функции perebor: короткие слова в 0 или 1 символ.
"""

from structs import Layout

def test_perebor_short_words_return_none():
    layout = Layout(name="test")
    
    assert layout.perebor("") is None
    assert layout.perebor("а") is None
    
    result = layout.perebor("ма")
    if result is None:
        print("⚠️  perebor('ма') вернул None (символы не найдены)")
    else:
        print("✅ perebor('ма') вернул результат")
    
    print("✅ Короткие слова обрабатываются правильно")
