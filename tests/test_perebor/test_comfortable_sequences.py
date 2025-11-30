# tests/test_perebor/test_comfortable_sequences.py
import pytest
from unittest.mock import patch


class TestPereborComfortableSequences:
    """Тесты удобных последовательностей"""

    def test_comfortable_left_hand_sequence(self, basic_layout, mock_key_left):
        """Тест удобной последовательности на левой руке"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            keys = [mock_key_left(code=30 + i) for i in range(4)]
            mock_choose.side_effect = keys

            result = basic_layout.perebor("тест")
            arm, conv, chl_count, chr_count = result

            assert chl_count['ch4'] == 1

    def test_comfortable_right_hand_sequence(self, basic_layout, mock_key_right):
        """Тест удобной последовательности на правой руке"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            keys = [mock_key_right(code=40 - i) for i in range(4)]
            mock_choose.side_effect = keys

            result = basic_layout.perebor("тест")
            arm, conv, chl_count, chr_count = result

            assert chr_count['ch4'] == 1

    def test_uncomfortable_left_hand_sequence(self, basic_layout, mock_key_left):
        """Тест неудобной последовательности на левой руке"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            keys = [mock_key_left(code=35 - i) for i in range(3)]
            mock_choose.side_effect = keys

            result = basic_layout.perebor("тест")
            arm, conv, chl_count, chr_count = result

            assert conv == 'bad'
            assert chl_count['ch2'] == 0
            assert chl_count['ch3'] == 0

    def test_uncomfortable_right_hand_sequence(self, basic_layout, mock_key_right):
        """Тест неудобной последовательности на правой руке"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            keys = [mock_key_right(code=35 + i) for i in range(3)]
            mock_choose.side_effect = keys

            result = basic_layout.perebor("тест")
            arm, conv, chl_count, chr_count = result

            assert conv == 'bad'
            assert chr_count['ch2'] == 0
            assert chr_count['ch3'] == 0