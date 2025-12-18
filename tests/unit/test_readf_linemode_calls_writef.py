"""
тестик на то что linemode вызывает writef
"""
from unittest.mock import patch, mock_open
from structs import Layout

def test_linemode_calls_writef():
    layout = Layout(name="test")
    
    with patch.object(layout, 'line_penalty_counter') as counter_mock, \
         patch.object(layout, 'writef') as writef_mock:
        
        counter_mock.return_value = (5, [0]*10, [0]*3)
        
        with patch('builtins.open', mock_open(read_data="hello\n")):
            layout.readf("any.txt", linemode=True)
            
            if writef_mock.called:
                print("✅ Всё ок! writef вызван")
            else:
                print("❌ Ошибка! writef НЕ вызван")
                assert False  # Завершаем тест с ошибкой
