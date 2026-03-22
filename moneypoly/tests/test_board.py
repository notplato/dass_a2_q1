import pytest

from moneypoly.board import Board
from moneypoly.config import (
    JAIL_POSITION,
    GO_TO_JAIL_POSITION,
    FREE_PARKING_POSITION,
    INCOME_TAX_POSITION,
    LUXURY_TAX_POSITION,
)


class DummyPlayer:
    def __init__(self, name):
        self.name = name

@pytest.fixture
def board():
    return Board()

@pytest.fixture
def player():
    return DummyPlayer("Player1")


def test_board_initialization(board):
    assert len(board.groups) == 8
    assert len(board.properties) == 22


def test_get_property_at_valid_branch(board):
    prop = board.get_property_at(1)
    assert prop is not None
    assert prop.name == "Mediterranean Avenue"

def test_get_property_at_invalid_branch(board):
    assert board.get_property_at(99) is None

def test_get_tile_type_special_branch(board):
    assert board.get_tile_type(0) == "go"
    assert board.get_tile_type(JAIL_POSITION) == "jail"
    assert board.get_tile_type(GO_TO_JAIL_POSITION) == "go_to_jail"
    assert board.get_tile_type(FREE_PARKING_POSITION) == "free_parking"
    assert board.get_tile_type(INCOME_TAX_POSITION) == "income_tax"
    assert board.get_tile_type(LUXURY_TAX_POSITION) == "luxury_tax"

def test_get_tile_type_property_branch(board):
    assert board.get_tile_type(1) == "property"

def test_get_tile_type_blank_branch(board):
    # position 12 is not in SPECIAL_TILES and has no Property
    assert board.get_tile_type(12) == "blank"

def test_is_purchasable_true_path(board):
    assert board.is_purchasable(1) is True

def test_is_purchasable_not_property_branch(board):
    assert board.is_purchasable(0) is False

def test_is_purchasable_railroad(board):
    assert board.is_purchasable(5) is True

def test_is_purchasable_mortgaged_branch(board):
    prop = board.get_property_at(1)
    prop.is_mortgaged = True
    assert board.is_purchasable(1) is False

def test_is_purchasable_owned_branch(board, player):
    prop = board.get_property_at(1)
    prop.owner = player
    assert board.is_purchasable(1) is False

def test_is_special_tile_true(board):
    assert board.is_special_tile(0) is True

def test_is_special_tile_false(board):
    assert board.is_special_tile(1) is False

def test_properties_owned_by(board, player):
    board.get_property_at(1).owner = player
    board.get_property_at(3).owner = player
    
    owned = board.properties_owned_by(player)
    assert len(owned) == 2
    assert owned[0].name == "Mediterranean Avenue"

def test_unowned_properties(board, player):
    board.get_property_at(1).owner = player
    
    unowned = board.unowned_properties()
    assert len(unowned) == 21