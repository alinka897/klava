# tests/test_line_penalty_counter/test_finger_distribution.py
import pytest
from unittest.mock import patch, Mock


class TestLinePenaltyCounterFingerDistribution:
    """Тесты распределения по пальцам для line_penalty_counter"""

    def test_line_penalty_counter_finger_distribution_left_hand(self, basic_layout):
        """Тест распределения по пальцам левой руки"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            # Левая рука - разные пальцы
            key_l_f5 = Mock()
            key_l_f5.arm = 'l'
            key_l_f5.finger = 'f5'
            key_l_f5.penalty = 1
            key_l_f5.alt = False

            key_l_f2 = Mock()
            key_l_f2.arm = 'l'
            key_l_f2.finger = 'f2'
            key_l_f2.penalty = 1
            key_l_f2.alt = False

            mock_choose.side_effect = [key_l_f5, key_l_f2]

            penalty, fingers, arms = basic_layout.line_penalty_counter("аб")

            # fingers: [lf5, lf4, lf3, lf2, rf2, rf3, rf4, rf5]
            assert fingers[0] == 1  # lf5
            assert fingers[3] == 1  # lf2

    def test_line_penalty_counter_finger_distribution_right_hand(self, basic_layout):
        """Тест распределения по пальцам правой руки"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            # Правая рука - разные пальцы
            key_r_f2 = Mock()
            key_r_f2.arm = 'r'
            key_r_f2.finger = 'f2'
            key_r_f2.penalty = 1
            key_r_f2.alt = False

            key_r_f5 = Mock()
            key_r_f5.arm = 'r'
            key_r_f5.finger = 'f5'
            key_r_f5.penalty = 1
            key_r_f5.alt = False

            mock_choose.side_effect = [key_r_f2, key_r_f5]

            penalty, fingers, arms = basic_layout.line_penalty_counter("аб")

            # fingers: [lf5, lf4, lf3, lf2, rf2, rf3, rf4, rf5]
            assert fingers[4] == 1  # rf2
            assert fingers[7] == 1  # rf5

    def test_line_penalty_counter_shift_finger_distribution(self, basic_layout, mock_key_left):
        """Тест распределения shift по пальцам"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            mock_choose.return_value = mock_key_left(code=30, penalty=1)

            penalty, fingers, arms = basic_layout.line_penalty_counter("АБВ")

            # Все три заглавные буквы - shift на правом мизинце
            assert fingers[7] == 3  # правый мизинец (shift)
