"""
тест функции возвращает Key или None
"""
from structs import Layout, Key

def test_choose_key_returns_key_or_none():
    
    layout = Layout(name="test")
    
    key = layout.choose_key("а")
    assert key is not None
    assert isinstance(key, Key)
    
    result = layout.choose_key("😀")
    assert result is None
    
    print("✅ choose_key возвращает правильные типы")
