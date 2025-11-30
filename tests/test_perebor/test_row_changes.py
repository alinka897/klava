# tests/test_perebor/test_row_changes.py
import pytest
from unittest.mock import patch


class TestPereborRowChanges:
    """Тесты смены рядов на одной руке"""

    def test_row_change_left_hand_comfortable(self, basic_layout, mock_key_left):
        """Тест удобной смены рядов на левой руке"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            mock_choose.side_effect = [
                mock_key_left(code=35, row='hr'),  # домашний ряд
                mock_key_left(code=20, row='ur')  # верхний ряд
            ]

            result = basic_layout.perebor("те")
            arm, conv, chl_count, chr_count = result

            assert conv == 'ok'

    def test_row_change_right_hand_comfortable(self, basic_layout, mock_key_right):
        """Тест удобной смены рядов на правой руке"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            mock_choose.side_effect = [
                mock_key_right(code=37, row='hr'),  # домашний ряд
                mock_key_right(code=23, row='ur')  # верхний ряд
            ]

            result = basic_layout.perebor("те")
            arm, conv, chl_count, chr_count = result

            assert conv == 'ok'

    def test_row_change_interrupts_sequence(self, basic_layout, mock_key_left):
        """Тест что смена ряда прерывает последовательность"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            mock_choose.side_effect = [
                mock_key_left(code=30, row='hr'),
                mock_key_left(code=31, row='hr'),  # удобно
                mock_key_left(code=20, row='ur'),  # смена ряда
                mock_key_left(code=21, row='ur'),  # новая последовательность
            ]

            result = basic_layout.perebor("слов")
            arm, conv, chl_count, chr_count = result

            # Должны быть две отдельные последовательности
            assert chl_count['ch2'] == 2