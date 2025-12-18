"""
тест нескольких символов на суммирование
"""
from structs import Layout

def test_line_penalty_counter_multiple_chars():
    layout = Layout(name="test")
    
    penalty1, fingers1, arms1 = layout.line_penalty_counter("а")
    penalty2, fingers2, arms2 = layout.line_penalty_counter("аа")
    
    assert penalty2 >= penalty1
    print("✅ при двойном нажатии штраф увеличивается")
