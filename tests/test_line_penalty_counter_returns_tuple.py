"""
Тест: функция возвращает кортеж из 3 элементов
"""
from structs import Layout

def test_line_penalty_counter_returns_tuple():
    """Тест: функция возвращает кортеж из 3 элементов"""
    layout = Layout(name="test")
    result = layout.line_penalty_counter("hello")
    
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert isinstance(result[0], int)  # penalty
    assert isinstance(result[1], list) # fingers
    assert len(result[1]) == 9         # 9 пальцев
    assert isinstance(result[2], list) # arms
    assert len(result[2]) == 3         # 3 категории рук
    print("✅ тут все гуд")
