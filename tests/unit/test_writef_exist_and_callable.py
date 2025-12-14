"""
тест writef существует
"""

def test_writef_exists():
    from structs import Layout
    
    layout = Layout(name="Тест")
    
    # 1. Метод есть
    assert hasattr(layout, 'writef'), "У Layout нет метода writef!"
    print("✅ Метод writef существует")
    
    # 2. Его можно вызвать
    assert callable(layout.writef), "writef нельзя вызвать!"
    print("✅ writef можно вызывать")
