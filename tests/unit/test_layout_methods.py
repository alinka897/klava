"""
проверка наличия методов класса layout
"""

def test_layouts_has_methods():
    from structs import Layout
    layout = Layout(name="test")

    assert hasattr(layout, '__init__'), "Нет метода __init__!"
    assert hasattr(layout, 'extract_keys'), "Нет метода extract_keys!"
    assert hasattr(layout, 'writef'), "Нет метода writef!"
    assert hasattr(layout, 'readf'), "Нет метода readf!"
    assert hasattr(layout, 'line_penalty_counter'), "Нет метода line_penalty_counter!"
    assert hasattr(layout, 'check_direction'), "Нет метода check_direction!"
    assert hasattr(layout, 'perebor'), "Нет метода perebor!"
    assert hasattr(layout, 'per_readf'), "Нет метода per_readf!"
    print(f"✅ Все методы класса layout существуют")
