"""
тест на то что неизвестные символы пропускаются
"""
from structs import Layout

def test_line_penalty_counter_unknown_chars():
    layout = Layout(name="test")
        
    penalty, fingers, arms = layout.line_penalty_counter("😀★§")
    
    assert penalty == 0
    print("✅ если символа нет, штраф не увеличивается")
