"""
Пробелы не должны учитываться (их нет в раскладке)
"""
from structs import Layout

def test_line_penalty_counter_with_spaces():
    
    layout = Layout(name="test")
    
    penalty_with_spaces, _, _ = layout.line_penalty_counter("а б в")
    penalty_without_spaces, _, _ = layout.line_penalty_counter("абв")
    
    assert abs(penalty_with_spaces - penalty_without_spaces) == 0
    print("✅ пробелы не учитываются, все гуд")
