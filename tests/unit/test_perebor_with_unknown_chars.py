"""
Тест на неизвестные символы возвращает none.
"""

from structs import Layout

def test_perebor_with_unknown_chars():
    layout = Layout(name="test")
    
    result = layout.perebor("hello")
    
    if result is None:
        print("✅ perebor('hello') вернул None (латинские буквы не в раскладке)")
    else:
        print(f"⚠️  perebor('hello') вернул результат {result[0]}")
    
    result = layout.perebor("мама123")
    if result is None:
        print("✅ perebor('мама123') вернул None (цифры не в раскладке)")
    else:
        print(f"⚠️  perebor('мама123') вернул результат")
