# tests/test_perebor/test_statistics.py
import pytest
from unittest.mock import patch


class TestPereborStatistics:
    """Тесты статистики последовательностей"""

    def test_multiple_sequences_same_hand(self, basic_layout, mock_key_left):
        """Тест нескольких последовательностей на одной руке"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            # Паттерн: удобно-неудобно-удобно
            mock_choose.side_effect = [
                mock_key_left(code=30),  # удобно
                mock_key_left(code=32),  # удобно
                mock_key_left(code=31),  # неудобно
                mock_key_left(code=33),  # удобно
                mock_key_left(code=34),  # удобно
            ]

            result = basic_layout.perebor("слово")
            arm, conv, chl_count, chr_count = result

            assert chl_count['ch2'] == 2
            assert chl_count['ch3'] == 0

    def test_sequence_across_hand_change(self, basic_layout, mock_key_left, mock_key_right):
        """Тест что последовательность прерывается при смене руки"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            mock_choose.side_effect = [
                mock_key_left(code=30),
                mock_key_left(code=31),
                mock_key_right(code=40),
                mock_key_right(code=39),
            ]

            result = basic_layout.perebor("тест")
            arm, conv, chl_count, chr_count = result

            assert chl_count['ch2'] == 1
            assert chr_count['ch2'] == 1

    def test_long_sequence_counting(self, basic_layout, mock_key_left):
        """Тест подсчета длинных последовательностей"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            keys = [mock_key_left(code=30 + i) for i in range(5)]
            mock_choose.side_effect = keys

            result = basic_layout.perebor("длинное")
            arm, conv, chl_count, chr_count = result

            assert chl_count['ch5'] == 1