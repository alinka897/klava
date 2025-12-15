"""
Одинаковые строки дают одинаковые результаты
"""
from structs import Layout

def test_line_penalty_counter_consistent():
    
    layout = Layout(name="test")
    
    result1 = layout.line_penalty_counter("test string")
    result2 = layout.line_penalty_counter("test string")
    
    assert result1 == result2
    print("✅ результаты идентичны")

