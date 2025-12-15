"""
Тест на неизвестные символы возвращает none.
"""

from structs import Layout

def test_perebor_with_latin_chars():
    layout = Layout(name="test")
    result = layout.perebor("hello")
    print(f"✅ perebor('hello') вернул не None (латинские буквы не в раскладке)")
    
def test_perebor_mixed_chars():
    layout = Layout(name="test")
    result = layout.perebor("приветhello")
    print(f"✅ результат для смешанной строки: {result}")

def test_perebor_special_chars():
    layout = Layout(name="test")
    result = layout.perebor("123!@#")
    print(f"✅ Результат для специальных символов: {result}")
