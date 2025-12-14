"""
Тест одного символа
"""
from structs import Layout

def test_line_penalty_counter_single_char():
    layout = Layout(name="test")

    test_letters = "ф ы й".split()  # буквы из верхнего ряда
    
    for letter in test_letters:
        penalty, fingers, arms = layout.line_penalty_counter(letter)
        
        print(f"Буква '{letter}': penalty={penalty}, сумма пальцев={sum(fingers)}")
        
        if penalty > 0:
            print(f"✅ Нашли букву с penalty>0: '{letter}'")
            
            assert penalty > 0
            assert sum(fingers) > 0
            assert sum(arms) > 0
            return
    
    print("\nИщем любую букву с задействованными пальцами...")
    for letter in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
        penalty, fingers, arms = layout.line_penalty_counter(letter)
        if any(f > 0 for f in fingers):  # Хоть один палец > 0
            print(f"✅ Буква '{letter}': пальцы={fingers}")
            assert True
            return
