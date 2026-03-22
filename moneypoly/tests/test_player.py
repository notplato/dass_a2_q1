import pytest

from moneypoly.player import Player
from moneypoly.config import STARTING_BALANCE, BOARD_SIZE, GO_SALARY, JAIL_POSITION

@pytest.fixture
def player():
    return Player("Test_Player")

def test_initialization_default(player):
    assert player.name == "Test_Player"
    assert player.balance == STARTING_BALANCE
    assert player.position == 0
    assert player.properties == []
    assert player.jail_props["in_jail"] is False
    assert player.jail_props["jail_turns"] == 0
    assert player.jail_props["get_out_of_jail_cards"] == 0
    assert player.is_eliminated is False

def test_initialization_custom():
    rich_player = Player("Richie", balance=5000)
    assert rich_player.name == "Richie"
    assert rich_player.balance == 5000
    assert rich_player.position == 0
    assert rich_player.properties == []
    assert rich_player.jail_props["in_jail"] is False
    assert rich_player.jail_props["jail_turns"] == 0
    assert rich_player.jail_props["get_out_of_jail_cards"] == 0
    assert rich_player.is_eliminated is False

def test_add_money_valid_branch(player):
    player.add_money(500)
    assert player.balance == STARTING_BALANCE + 500

def test_add_money_negative_branch(player):
    with pytest.raises(ValueError):
        player.add_money(-100)

def test_deduct_money_valid_branch(player):
    player.deduct_money(500)
    assert player.balance == STARTING_BALANCE - 500

def test_deduct_money_negative_branch(player):
    with pytest.raises(ValueError):
        player.deduct_money(-100)

def test_is_bankrupt_true_path(player):
    player.balance = 0
    assert player.is_bankrupt() is True
    
    player.balance = -50
    assert player.is_bankrupt() is True

def test_is_bankrupt_false_path(player):
    assert player.is_bankrupt() is False

def test_net_worth(player):
    player.balance = 1000
    dummy_property = {"name": "Boardwalk", "price": 400}
    player.add_property(dummy_property)
    
    assert player.net_worth() == 1000

def test_move_lands_exactly_on_go_branch(player):
    player.position = BOARD_SIZE - 2 
    
    new_pos = player.move(2)
    
    assert new_pos == 0
    assert player.position == 0
    assert player.balance == STARTING_BALANCE + GO_SALARY

def test_move_passes_go_bug(player):
    player.position = BOARD_SIZE - 2 
    
    new_pos = player.move(5)
    
    assert new_pos == 3
    assert player.position == 3
    assert player.balance == STARTING_BALANCE + GO_SALARY

def test_go_to_jail(player):
    player.go_to_jail()
    assert player.position == JAIL_POSITION
    assert player.jail_props["in_jail"] is True
    assert player.jail_props["jail_turns"] == 0

def test_add_property_new_branch(player):
    player.add_property("Park Place")
    assert "Park Place" in player.properties
    assert player.count_properties() == 1

def test_add_property_duplicate_branch(player):
    player.add_property("Boardwalk")
    player.add_property("Boardwalk")
    assert player.count_properties() == 1

def test_remove_property_existing_branch(player):
    player.add_property("Baltic Ave")
    player.remove_property("Baltic Ave")
    assert player.count_properties() == 0

def test_remove_property_nonexistent_branch(player):
    player.add_property("Baltic Ave")
    player.remove_property("Boardwalk")
    assert player.count_properties() == 1
    assert "Baltic Ave" in player.properties