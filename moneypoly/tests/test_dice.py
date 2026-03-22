import pytest

import pytest
from unittest.mock import patch

from moneypoly.dice import Dice

@pytest.fixture
def dice():
    return Dice()

def test_initial_state(dice):
    assert dice.die1 == 0
    assert dice.die2 == 0
    assert dice.doubles_streak == 0

def test_reset(dice):
    dice.die1 = 3
    dice.die2 = 5
    dice.doubles_streak = 2
    
    dice.reset()
    assert dice.die1 == 0
    assert dice.die2 == 0
    assert dice.doubles_streak == 0


@patch('random.randint')
def test_roll_doubles_branch(mock_randint, dice):
    mock_randint.side_effect = [4, 4]
    
    total = dice.roll()
    
    assert total == 8
    assert dice.die1 == 4
    assert dice.die2 == 4
    assert dice.doubles_streak == 1  # streak increments

@patch('random.randint')
def test_roll_non_doubles_branch(mock_randint, dice):
    dice.doubles_streak = 1
    
    mock_randint.side_effect = [3, 5]
    
    total = dice.roll()
    
    assert total == 8
    assert dice.die1 == 3
    assert dice.die2 == 5
    assert dice.doubles_streak == 0  # Streak resets to 0

def test_is_doubles_true_path(dice):
    dice.die1 = 2
    dice.die2 = 2
    assert dice.is_doubles() is True

def test_is_doubles_false_path(dice):
    dice.die1 = 2
    dice.die2 = 3
    assert dice.is_doubles() is False

def test_total_calculation(dice):
    dice.die1 = 5
    dice.die2 = 6
    assert dice.total() == 11

def test_describe_doubles_branch(dice):
    dice.die1 = 6
    dice.die2 = 6
    assert dice.describe() == "6 + 6 = 12 (DOUBLES)"

def test_describe_non_doubles_branch(dice):
    dice.die1 = 2
    dice.die2 = 3
    assert dice.describe() == "2 + 3 = 5"

def test_doubles_initial_state(dice):
    assert dice.is_doubles() == False

def test_six_sides(dice):
    seen_six = False
    
    # roll a hundered times to (try) get a 6
    for _ in range(100):
        dice.roll()
        if dice.die1 == 6 or dice.die2 == 6:
            seen_six = True
            
    assert seen_six is True