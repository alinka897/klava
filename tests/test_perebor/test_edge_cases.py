# tests/test_perebor/test_edge_cases.py
import pytest
from unittest.mock import patch


class TestPereborEdgeCases:
    """Тесты граничных случаев для функции perebor"""

    def test_perebor_empty_string(self, basic_layout):
        """Тест пустой строки"""
        result = basic_layout.perebor("")
        assert result is None

    def test_perebor_single_character(self, basic_layout):
        """Тест одного символа"""
        result = basic_layout.perebor("а")
        assert result is None

    def test_perebor_only_punctuation(self, basic_layout):
        """Тест только пунктуации"""
        result = basic_layout.perebor("!!!")
        assert result is None

    def test_perebor_strips_punctuation(self, basic_layout, mock_key_left, mock_key_right):
        """Тест удаления пунктуации вокруг слова"""
        with patch.object(basic_layout, 'choose_key') as mock_choose:
            mock_choose.side_effect = [
                mock_key_left(code=30),
                mock_key_right(code=40)
            ]

            result = basic_layout.perebor("  слово!  ")
            assert result is not None
            assert mock_choose.call_count == 2