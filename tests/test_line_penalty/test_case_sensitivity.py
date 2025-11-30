# tests/test_line_penalty_counter/test_case_sensitivity.py
import pytest
from unittest.mock import patch


class TestLinePenaltyCounterCaseSensitivity:
    """Тесты регистрозависимости для line_penalty_counter"""

    def test_line_penalty_counter_uppercase_letters(self, basic_layout, mock_key_left):
        """Тест заглавных букв (добавляется штраф за shift)"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            mock_choose.return_value = mock_key_left(code=30, penalty=1)

            penalty, fingers, arms = basic_layout.line_penalty_counter("Абв")

            # 'А' - заглавная: penalty=1 + shift=1 = 2
            # 'б', 'в' - строчные: penalty=1 каждый
            assert penalty == 4
            # Проверяем что shift учтен для правого мизинца
            assert fingers[7] >= 1  # правый мизинец (shift)

    def test_line_penalty_counter_mixed_case(self, basic_layout, mock_key_left, mock_key_right):
        """Тест смешанного регистра"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            # Чередуем левую и правую руку
            mock_choose.side_effect = [
                mock_key_left(code=30, penalty=1),  # 'А' - заглавная
                mock_key_right(code=40, penalty=1),  # 'б' - строчная
                mock_key_left(code=31, penalty=1),  # 'В' - заглавная
            ]

            penalty, fingers, arms = basic_layout.line_penalty_counter("АбВ")

            # А: 1(penalty) + 1(shift) = 2
            # б: 1(penalty) = 1
            # В: 1(penalty) + 1(shift) = 2
            assert penalty == 5
            assert arms[1] >= 2  # двуручие (за shift)

    def test_line_penalty_counter_all_uppercase(self, basic_layout, mock_key_left):
        """Тест всех заглавных букв"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            mock_choose.return_value = mock_key_left(code=30, penalty=1)

            penalty, fingers, arms = basic_layout.line_penalty_counter("АБВ")

            # 3 буквы × (penalty=1 + shift=1) = 6
            assert penalty == 6
            assert fingers[7] == 3  # правый мизинец (shift для каждой буквы)
