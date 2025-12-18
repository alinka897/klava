"""
тест на то что в readf все хорошо считается
"""
from structs import Layout
from unittest.mock import patch, mock_open

def test_readf_sums_correctly():
    layout = Layout(name="test")
    
    with patch.object(layout, 'line_penalty_counter') as mock_counter:
        mock_counter.side_effect = [
            (5, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0]),
            (3, [0, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0]),
        ]
        
        with patch('builtins.open', mock_open(read_data="line1\nline2\n")):
            penalty, fingers, arms = layout.readf("test.txt")
            
            assert penalty == 8
            print("✅ суммирование штрафа прошло успешно")
            assert fingers == [1, 2, 0, 0, 0, 0, 0, 0, 0, 0]
            print("✅ суммирование пальцев успешно")
            assert arms == [1, 1, 0]
            print("✅ суммирование рук успешно")
