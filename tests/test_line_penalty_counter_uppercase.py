"""
тест на то что у заглавных букв штраф больше
"""
from structs import Layout

def test_line_penalty_counter_uppercase():
    layout = Layout(name="test")
    
    penalty_lower, _, _ = layout.line_penalty_counter("а")
    penalty_upper, _, _ = layout.line_penalty_counter("А")
    
    assert penalty_upper > penalty_lower
    print("✅ у заглавных штраф больше, все гуд")


