# tests/test_perebor/test_complex_scenarios.py
import pytest
from unittest.mock import patch


class TestPereborComplexScenarios:
    """Тесты сложных сценариев"""

    def test_mixed_pattern(self, basic_layout, mock_key_left, mock_key_right):
        """Тест сложного смешанного паттерна"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            mock_choose.side_effect = [
                mock_key_left(code=30),
                mock_key_left(code=31),
                mock_key_right(code=40),
                mock_key_right(code=39),
                mock_key_right(code=38),
                mock_key_right(code=25, row='ur'),
            ]

            result = basic_layout.perebor("сложно")
            arm, conv, chl_count, chr_count = result

            assert arm == 'both'
            assert chl_count['ch2'] == 1
            assert chr_count['ch3'] == 1

    def test_unknown_character_returns_none(self, basic_layout):
        """Тест что неизвестный символ возвращает None"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            mock_choose.return_value = None

            result = basic_layout.perebor("test")
            assert result is None

    def test_combination_all_patterns(self, basic_layout, mock_key_left, mock_key_right):
        """Тест комбинации всех паттернов в одном слове"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            mock_choose.side_effect = [
                # Удобная последовательность на левой
                mock_key_left(code=30),
                mock_key_left(code=31),
                # Смена на правую
                mock_key_right(code=40),
                # Удобная последовательность на правой
                mock_key_right(code=39),
                # Смена ряда
                mock_key_right(code=25, row='ur'),
                # Обратно на левую
                mock_key_left(code=32),
            ]


            result = basic_layout.perebor("комбинация")
            assert result is not None
            arm, conv, chl_count, chr_count = result

            assert arm == 'both'