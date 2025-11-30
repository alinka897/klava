# tests/test_perebor/test_hand_usage.py
import pytest
from unittest.mock import patch


class TestPereborHandUsage:
    """Тесты определения используемых рук"""

    def test_perebor_only_left_hand(self, basic_layout, mock_key_left):
        """Тест слова только на левой руке"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            keys = [mock_key_left(code=30 + i) for i in range(3)]
            mock_choose.side_effect = keys

            result = basic_layout.perebor("тест")
            arm, conv, chl_count, chr_count = result

            assert arm == 'l'

    def test_perebor_only_right_hand(self, basic_layout, mock_key_right):
        """Тест слова только на правой руке"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            keys = [mock_key_right(code=40 - i) for i in range(3)]
            mock_choose.side_effect = keys

            result = basic_layout.perebor("тест")
            arm, conv, chl_count, chr_count = result

            assert arm == 'r'

    def test_perebor_both_hands(self, basic_layout, mock_key_left, mock_key_right):
        """Тест слова с обеими руками"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            mock_choose.side_effect = [
                mock_key_left(code=30),
                mock_key_right(code=40),
                mock_key_left(code=31)
            ]

            result = basic_layout.perebor("тест")
            arm, conv, chl_count, chr_count = result

            assert arm == 'both'
            assert conv == 'bad'