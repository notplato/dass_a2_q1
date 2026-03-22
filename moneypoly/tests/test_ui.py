import pytest
from unittest.mock import patch

from moneypoly import ui

def test_format_currency():
    assert ui.format_currency(1500000) == "$1,500,000"
    assert ui.format_currency(0) == "$0"

@patch('builtins.input', return_value='42')
def test_safe_int_input_valid(mock_input):
    result = ui.safe_int_input("Enter number:")
    assert result == 42

@patch('builtins.input', return_value='not a number')
def test_safe_int_input_invalid_branch(mock_input):
    result = ui.safe_int_input("Enter number:", default=99)
    assert result == 99

@patch('builtins.input', return_value='  Y  ')
def test_confirm_true_branch(mock_input):
    assert ui.confirm("Are you sure?") is True

@patch('builtins.input', side_effect=['n', 'yes', ''])
def test_confirm_false_branch(mock_input):
    assert ui.confirm("Are you sure?") is False # 'n'
    assert ui.confirm("Are you sure?") is False # 'yes' (only exact 'y' works)
    assert ui.confirm("Are you sure?") is False # empty string