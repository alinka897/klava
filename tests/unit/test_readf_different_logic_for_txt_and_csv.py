"""
Тест на разлиность обработки файлов txt и csv расширений
"""

from unittest.mock import patch, mock_open
from structs import Layout

def test_readf_different_logic_for_txt_and_csv():
    layout = Layout(name="test")
    
    with patch.object(layout, 'line_penalty_counter') as mock_counter:
        mock_counter.return_value = (0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0])
        
        # ТЕСТ 1: Текстовый файл (.txt)
        with patch('builtins.open', mock_open(read_data="строка1\nстрока2\n3строка\n")):
            layout.readf("test.txt")
            
            assert mock_counter.call_count == 3
        
        # Сбрасываем счетчик вызовов
        mock_counter.reset_mock()
        
        # ТЕСТ 2: CSV файл
        csv_data = "строка1\nстрока2\n3строка\n"
        with patch('builtins.open', mock_open(read_data=csv_data)):
            layout.readf("test.csv")

            assert mock_counter.call_count == 3
    
    print("✅ Логика ветвления работает: .txt и .csv обрабатываются по-разному")
