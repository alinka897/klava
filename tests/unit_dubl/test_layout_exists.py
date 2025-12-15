"""
Layout создается
"""
def test_layout_exists():
    from structs import Layout

    # Создаем раскладку
    layout = Layout(name="Тестовая раскладка")
    
    # Проверяем что объект создан
    assert layout is not None
    print("✅ Layout создан!")
    
    # Проверяем имя
    assert layout.name == "Тестовая раскладка"
    print(f"✅ Имя раскладки: {layout.name}")
