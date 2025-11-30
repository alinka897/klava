# tests/test_line_penalty_counter/test_complex_scenarios.py
import pytest
from unittest.mock import patch, Mock


class TestLinePenaltyCounterComplexScenarios:
    """Тесты сложных сценариев для line_penalty_counter"""

    def test_line_penalty_counter_complex_scenario(self, basic_layout):
        """Тест сложного сценария со всеми типами штрафов"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            # Заглавная с alt на левой руке
            key1 = Mock()
            key1.arm = 'l'
            key1.finger = 'f2'
            key1.penalty = 2
            key1.alt = True

            # Строчная на правой руке
            key2 = Mock()
            key2.arm = 'r'
            key2.finger = 'f3'
            key2.penalty = 1
            key2.alt = False

            mock_choose.side_effect = [key1, key2]

            penalty, fingers, arms = basic_layout.line_penalty_counter("Аб")

            # А: penalty=2 + alt=1 + shift=1 = 4
            # б: penalty=1 = 1
            assert penalty == 5
            # Проверяем распределение по рукам
            assert arms[1] > 0  # двуручие (shift + alt)

    def test_line_penalty_counter_arm_calculation(self, basic_layout, mock_key_left, mock_key_right):
        """Тест расчета нагрузки на руки"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            # 2 левых, 1 правой
            mock_choose.side_effect = [
                mock_key_left(penalty=1),
                mock_key_left(penalty=1),
                mock_key_right(penalty=1)
            ]

            penalty, fingers, arms = basic_layout.line_penalty_counter("абв")

            # arms: [левая, двуручие, правая]
            assert arms[0] == 2  # левая рука
            assert arms[2] == 1  # правая рука
            assert arms[1] == 0  # нет двуручия

    def test_line_penalty_counter_mixed_hands_and_modifiers(self, basic_layout):
        """Тест смешанных рук и модификаторов"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            # Разные комбинации рук и модификаторов
            keys = [
                Mock(arm='l', penalty=1, alt=False),  # левая, строчная
                Mock(arm='r', penalty=2, alt=True),  # правая, alt
                Mock(arm='l', penalty=1, alt=False),  # левая, заглавная (shift)
            ]

            mock_choose.side_effect = keys

            penalty, fingers, arms = basic_layout.line_penalty_counter("аБв")

            # а: 1
            # Б: 2 + 1(alt) = 3
            # в: 1 + 1(shift) = 2
            assert penalty == 6
            # Проверяем распределение
            assert arms[0] > 0  # левая
            assert arms[1] > 0  # двуручие
            assert arms[2] > 0  # правая