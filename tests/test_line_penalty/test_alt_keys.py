# tests/test_line_penalty_counter/test_alt_keys.py
import pytest
from unittest.mock import patch, Mock


class TestLinePenaltyCounterAltKeys:
    """Тесты для alt-клавиш в line_penalty_counter"""

    def test_line_penalty_counter_alt_key_penalty_left_hand(self, basic_layout):
        """Тест штрафа за alt-клавиши на левой руке"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            # Создаем mock для alt-клавиши на левой руке
            alt_key = Mock()
            alt_key.arm = 'l'
            alt_key.penalty = 1
            alt_key.alt = True
            alt_key.finger = 'f2'

            mock_choose.return_value = alt_key

            penalty, fingers, arms = basic_layout.line_penalty_counter("а")

            # penalty=1 + alt=1
            assert penalty == 2
            # alt на левой руке учитывается в двуручии
            assert arms[1] >= 1

    def test_line_penalty_counter_alt_key_penalty_right_hand(self, basic_layout):
        """Тест штрафа за alt-клавиши на правой руке"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            # Создаем mock для alt-клавиши на правой руке
            alt_key = Mock()
            alt_key.arm = 'r'
            alt_key.penalty = 1
            alt_key.alt = True
            alt_key.finger = 'f2'

            mock_choose.return_value = alt_key

            penalty, fingers, arms = basic_layout.line_penalty_counter("а")

            # penalty=1 + alt=1
            assert penalty == 2
            # alt на правой руке учитывается в правой руке
            assert arms[2] >= 1

    def test_line_penalty_counter_alt_key_with_uppercase(self, basic_layout):
        """Тест alt-клавиши с заглавной буквой"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            alt_key = Mock()
            alt_key.arm = 'l'
            alt_key.penalty = 2
            alt_key.alt = True
            alt_key.finger = 'f2'

            mock_choose.return_value = alt_key

            penalty, fingers, arms = basic_layout.line_penalty_counter("А")

            # penalty=2 + alt=1 + shift=1 = 4
            assert penalty == 4
            # Должен быть shift и alt
            assert arms[1] >= 2  # двуручие
