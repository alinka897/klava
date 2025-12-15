"""
тестик на нул строку
"""
from structs import Layout

def test_line_penalty_counter_empty_string():
    layout = Layout(name="test")
    penalty, fingers, arms = layout.line_penalty_counter("")
    
    assert penalty == 0
    assert all(f == 0 for f in fingers)
    assert all(a == 0 for a in arms)
    print("✅ нул строка = все по нулям")
