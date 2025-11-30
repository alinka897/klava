# tests/test_line_penalty_counter/test_basic_cases.py
import pytest
from unittest.mock import patch


class TestLinePenaltyCounterBasicCases:
    """Базовые тесты для line_penalty_counter"""

    def test_line_penalty_counter_empty_string(self, basic_layout):
        """Тест пустой строки"""
        penalty, fingers, arms = basic_layout.line_penalty_counter("")
        assert penalty == 0
        assert all(count == 0 for count in fingers)
        assert all(count == 0 for count in arms)

    def test_line_penalty_counter_only_letters(self, basic_layout, mock_key_left):
        """Тест строки только с буквами"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            mock_choose.return_value = mock_key_left(code=30, penalty=1)

            penalty, fingers, arms = basic_layout.line_penalty_counter("абв")

            assert penalty == 3  # 3 буквы × penalty=1
            assert fingers[0] == 3  # левый мизинец
            assert arms[0] == 3  # левая рука

    def test_line_penalty_counter_ignores_non_alpha(self, basic_layout, mock_key_left):
        """Тест что не-буквенные символы игнорируются"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            mock_choose.return_value = mock_key_left(code=30, penalty=1)

            penalty, fingers, arms = basic_layout.line_penalty_counter("а 123 б! в")

            # Только 3 буквы: а, б, в
            assert penalty == 3
            assert mock_choose.call_count == 3

    def test_line_penalty_counter_unknown_character_skipped(self, basic_layout):
        """Тест что неизвестные символы пропускаются"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            mock_choose.side_effect = [None, Mock(arm='l', penalty=1), None]

            penalty, fingers, arms = basic_layout.line_penalty_counter("1а2")

            # Только одна буква 'а' обработана
            assert penalty == 1
            assert mock_choose.call_count == 3