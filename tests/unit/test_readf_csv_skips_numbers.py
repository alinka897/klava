"""
тест CSV должен пропускать цифры 
"""

from unittest.mock import patch, mock_open
from structs import Layout

def test_readf_csv_skips_numbers():
    layout = Layout(name="test")
    
    with patch.object(layout, 'line_penalty_counter') as mock_counter:
        mock_counter.return_value = (5, [1]*9, [1]*3)

        csv_only_numbers = "123,456\n789,000\n"
        with patch('builtins.open', mock_open(read_data=csv_only_numbers)):
            penalty, fingers, arms = layout.readf("test.csv")
            
            # line_penalty_counter НЕ должен вызываться
            assert mock_counter.call_count == 0
            # Результаты должны быть нулевыми
            assert penalty == 0
            assert all(f == 0 for f in fingers)
            assert all(a == 0 for a in arms)
    
    print("✅ CSV правильно пропускает числовые значения")
