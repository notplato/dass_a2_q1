import pytest
from unittest.mock import patch, MagicMock

from moneypoly.game import Game
from moneypoly.config import (
    STARTING_BALANCE, INCOME_TAX_AMOUNT, LUXURY_TAX_AMOUNT,
    JAIL_FINE, GO_SALARY, MAX_TURNS, JAIL_POSITION, AUCTION_MIN_INCREMENT
)

@pytest.fixture
def game():
    return Game(["Alice", "Bob"])

@pytest.fixture
def alice(game):
    return game.players[0]

@pytest.fixture
def bob(game):
    return game.players[1]

@pytest.fixture
def prop(game):
    return game.state["board"].properties[0] # Mediterranean Ave

def test_game_initialization(game, alice, bob):
    assert len(game.players) == 2
    assert alice.name == "Alice"
    assert bob.name == "Bob"
    assert game.current_index == 0
    assert game.turn_number == 0
    assert game.running == True

def test_current_player(game, alice, bob):
    assert game.current_player() == alice
    game.advance_turn()
    assert game.current_player() == bob

def test_advance_turn(game):
    game.advance_turn()
    assert game.current_index == 1
    game.advance_turn()
    assert game.current_index == 0

@patch('moneypoly.game.Game._handle_jail_turn')
def test_play_turn_in_jail(mock_jail, game, alice):
    alice.in_jail = True
    game.play_turn()
    mock_jail.assert_called_once_with(alice)
    assert game.current_index == 1

@patch('moneypoly.dice.Dice.roll', return_value=5)
@patch('moneypoly.dice.Dice.is_doubles', return_value=False)
@patch('moneypoly.game.Game._move_and_resolve')
def test_play_turn_standard(mock_move, mock_doubles, mock_roll, game, alice):
    game.play_turn()
    mock_move.assert_called_once_with(alice, 5)
    assert game.current_index == 1

@patch('moneypoly.dice.Dice.roll', return_value=4)
@patch('moneypoly.dice.Dice.is_doubles', return_value=True)
@patch('moneypoly.game.Game._move_and_resolve')
def test_play_turn_doubles_extra_roll(mock_move, mock_doubles, mock_roll, game):
    game.state["dice"].doubles_streak = 1
    game.play_turn()
    assert game.current_index == 0

@patch('moneypoly.dice.Dice.roll', return_value=4)
def test_play_turn_speeding_jail(mock_roll, game, alice):
    game.state["dice"].doubles_streak = 3
    game.play_turn()
    assert alice.position == JAIL_POSITION
    assert alice.jail_props["in_jail"] is True
    assert game.current_index == 1

def test_resolve_go_to_jail(game, alice):
    game._move_and_resolve(alice, 30)
    assert alice.position == JAIL_POSITION
    assert alice.jail_props["in_jail"] is True

def test_resolve_income_tax(game, alice):
    game.state["board"].get_tile_type = MagicMock(return_value="income_tax")
    game._move_and_resolve(alice, 4)
    assert alice.balance == STARTING_BALANCE - INCOME_TAX_AMOUNT

def test_resolve_luxury_tax(game, alice):
    game.state["board"].get_tile_type = MagicMock(return_value="luxury_tax")
    game._move_and_resolve(alice, 38)
    assert alice.balance == STARTING_BALANCE - LUXURY_TAX_AMOUNT

def test_resolve_free_parking(game, alice):
    game.state["board"].get_tile_type = MagicMock(return_value="free_parking")
    game._move_and_resolve(alice, 20)
    assert alice.balance == STARTING_BALANCE

@patch('moneypoly.game.Game._apply_card')
def test_resolve_chance_and_community_chest(mock_apply, game, alice):
    game.state["board"].get_tile_type = MagicMock(return_value="chance")
    game._move_and_resolve(alice, 7)
    mock_apply.assert_called_once()
    
    game.state["board"].get_tile_type = MagicMock(return_value="community_chest")
    game._move_and_resolve(alice, 2)
    assert mock_apply.call_count == 2

@patch('moneypoly.game.Game._handle_property_tile')
def test_resolve_property_and_railroad(mock_handle, game, alice, prop):
    game.state["board"].get_tile_type = MagicMock(return_value="property")
    game.state["board"].get_property_at = MagicMock(return_value=prop)
    game._move_and_resolve(alice, 1)
    mock_handle.assert_called_once_with(alice, prop)

@patch('builtins.input', return_value='b')
@patch('moneypoly.game.Game.buy_property')
def test_handle_unowned_buy(mock_buy, mock_input, game, alice, prop):
    game._handle_property_tile(alice, prop)
    mock_buy.assert_called_once_with(alice, prop)

@patch('builtins.input', return_value='a')
@patch('moneypoly.game.Game.auction_property')
def test_handle_unowned_auction(mock_auction, mock_input, game, alice, prop):
    game._handle_property_tile(alice, prop)
    mock_auction.assert_called_once_with(prop)

@patch('builtins.input', return_value='s')
def test_handle_unowned_skip(mock_input, game, alice, prop):
    game._handle_property_tile(alice, prop)

def test_handle_owned_by_self(game, alice, prop):
    prop.owner = alice
    game._handle_property_tile(alice, prop) # should print and return

@patch('moneypoly.game.Game.pay_rent')
def test_handle_owned_by_other(mock_pay, game, alice, bob, prop):
    prop.owner = bob
    game._handle_property_tile(alice, prop)
    mock_pay.assert_called_once_with(alice, prop)

def test_buy_property_success_branch(game, alice, prop):
    success = game.buy_property(alice, prop)
    
    assert success is True
    assert prop.owner == alice
    assert prop in alice.properties
    assert alice.balance == STARTING_BALANCE - prop.stats["price"]

def test_buy_property_insufficient_funds_branch(game, alice, prop):
    alice.balance = 10 # make alice broke
    success = game.buy_property(alice, prop)
    
    assert success is False
    assert prop.owner is None
    assert alice.balance == 10

def test_pay_rent(game, alice, bob, prop):
    prop.owner = bob
    game.pay_rent(alice, prop)
    assert alice.balance == STARTING_BALANCE - prop.get_rent()
    assert bob.balance == STARTING_BALANCE + prop.get_rent()

def test_pay_rent_mortgaged_branch(game, alice, bob, prop):
    prop.owner = bob
    prop.is_mortgaged = True
    
    game.pay_rent(alice, prop)
    assert alice.balance == STARTING_BALANCE

def test_mortgage_and_unmortgage_flow(game, alice, prop):
    prop.owner = alice
    
    game.mortgage_property(alice, prop)
    assert prop.is_mortgaged is True
    assert alice.balance == STARTING_BALANCE + prop.stats["mortgage_value"]
    
    cost = int(prop.stats["mortgage_value"] * 1.1)
    game.unmortgage_property(alice, prop)
    assert prop.is_mortgaged is False
    assert alice.balance == (STARTING_BALANCE + prop.stats["mortgage_value"]) - cost

def test_mortgage_wrong_owner(game, alice, bob, prop):
    prop.owner = alice
    
    game.mortgage_property(bob, prop)
    assert prop.is_mortgaged is False

def test_mortgage_remortgage(game, alice, prop):
    prop.owner = alice
    
    game.mortgage_property(alice, prop)
    retval = game.mortgage_property(alice, prop)
    assert prop.is_mortgaged is True
    assert retval is False
    assert alice.balance == STARTING_BALANCE + prop.stats["mortgage_value"]

def test_trade(game, alice, bob, prop):
    prop.owner = alice
    game.trade(seller=alice, buyer=bob, prop=prop, cash_amount=100)
    assert bob.balance == STARTING_BALANCE - 100
    assert prop.owner == bob
    assert prop in bob.properties
    assert prop not in alice.properties
    assert alice.balance == STARTING_BALANCE + 100

def test_trade_wrong_owner(game, alice, bob, prop):
    prop.owner = alice
    retval = game.trade(seller=bob, buyer=alice, prop=prop, cash_amount=100)
    assert retval is False

def test_trade_insufficient_funds(game, alice, bob, prop):
    prop.owner = alice
    bob.balance = 10
    retval = game.trade(seller=alice, buyer=bob, prop=prop, cash_amount=100)
    assert retval is False

@patch('moneypoly.ui.safe_int_input', side_effect=[0, 0])
def test_auction_all_pass_branch(mock_input, game, alice, bob, prop):
    game.auction_property(prop)
    
    assert prop.owner is None
    assert alice.balance == STARTING_BALANCE
    assert bob.balance == STARTING_BALANCE

@patch('moneypoly.ui.safe_int_input')
def test_auction_bid_too_low_branch(mock_input, game, alice, bob, prop):
    invalid_bid = AUCTION_MIN_INCREMENT - 1
    mock_input.side_effect = [invalid_bid, 0]
    
    game.auction_property(prop)
    
    assert prop.owner is None

@patch('moneypoly.ui.safe_int_input')
def test_auction_cannot_afford_branch(mock_input, game, alice, bob, prop):
    too_high_bid = STARTING_BALANCE + 500
    mock_input.side_effect = [too_high_bid, 0]
    
    game.auction_property(prop)
    
    assert prop.owner is None

@patch('moneypoly.ui.safe_int_input')
def test_auction_valid_bidding_and_winner_branch(mock_input, game, alice, bob, prop):
    alice_bid = AUCTION_MIN_INCREMENT
    bob_bid = AUCTION_MIN_INCREMENT * 2
    mock_input.side_effect = [alice_bid, bob_bid]
    
    game.auction_property(prop)
    
    assert prop.owner == bob
    assert prop in bob.properties
    assert bob.balance == STARTING_BALANCE - bob_bid
    
    assert alice.balance == STARTING_BALANCE

@patch('moneypoly.game.Game._move_and_resolve') # stops the player from moving after release
@patch('moneypoly.ui.confirm', return_value=True)
def test_jail_use_card(mock_confirm, mock_move, game, alice):
    alice.in_jail = True
    alice.jail_turns = 1
    alice.get_out_of_jail_cards = 1
    game._handle_jail_turn(alice)
    
    assert alice.get_out_of_jail_cards == 0
    assert alice.in_jail is False
    mock_move.assert_called_once()

@patch('moneypoly.game.Game._move_and_resolve')
@patch('moneypoly.ui.confirm', side_effect=[False, True]) # No to card, Yes to fine
def test_jail_pay_fine(mock_confirm, mock_move, game, alice):
    alice.in_jail = True
    alice.get_out_of_jail_cards = 1
    game._handle_jail_turn(alice)
    
    assert alice.in_jail is False
    assert alice.balance == STARTING_BALANCE - JAIL_FINE
    assert alice.get_out_of_jail_cards == 1
    mock_move.assert_called_once()

@patch('moneypoly.game.Game._move_and_resolve')
@patch('moneypoly.ui.confirm', return_value=False)
def test_jail_serve_time(mock_confirm, mock_move, game, alice):
    """Test branch where player waits."""
    alice.in_jail = True
    alice.jail_turns = 1
    game._handle_jail_turn(alice)
    
    assert alice.in_jail is True
    assert alice.jail_turns == 2
    mock_move.assert_not_called()

@patch('moneypoly.game.Game._move_and_resolve')
@patch('moneypoly.ui.confirm', return_value=False)
def test_jail_mandatory_release(mock_confirm, mock_move, game, alice):
    """Test branch where player hits 3 turns and is forced out."""
    alice.in_jail = True
    alice.jail_turns = 2
    game._handle_jail_turn(alice)
    
    assert alice.in_jail is False
    assert alice.jail_turns == 0
    assert alice.balance == STARTING_BALANCE - JAIL_FINE
    mock_move.assert_called_once()

def test_apply_card_collect(game, alice):
    card = {"description": "Test", "action": "collect", "value": 50}
    game._apply_card(alice, card)
    assert alice.balance == STARTING_BALANCE + 50

def test_apply_card_pay(game, alice):
    card = {"description": "Test", "action": "pay", "value": 50}
    game._apply_card(alice, card)
    assert alice.balance == STARTING_BALANCE - 50

def test_apply_card_jail(game, alice):
    card = {"description": "Test", "action": "jail", "value": 0}
    game._apply_card(alice, card)
    assert alice.position == JAIL_POSITION
    assert alice.jail_props["in_jail"] is True

def test_apply_card_jail_free(game, alice):
    card = {"description": "Test", "action": "jail_free", "value": 0}
    game._apply_card(alice, card)
    assert alice.get_out_of_jail_cards == 1

def test_apply_card_move_to_pass_go(game, alice):
    alice.position = 35
    card = {"description": "Test", "action": "move_to", "value": 5}
    game._apply_card(alice, card)
    assert alice.position == 5
    assert alice.balance == STARTING_BALANCE + GO_SALARY

def test_apply_card_collect_from_all(game, alice, bob):
    card = {"description": "Test", "action": "collect_from_all", "value": 10}
    game._apply_card(alice, card)
    assert bob.balance == STARTING_BALANCE - 10
    assert alice.balance == STARTING_BALANCE + 10

def test_check_bankruptcy(game, alice, prop):
    prop.owner = alice
    alice.properties.append(prop)
    alice.balance = -10
    game._check_bankruptcy(alice)
    
    assert alice.is_eliminated is True
    assert prop.owner is None
    assert alice not in game.players

def test_find_winner(game, alice, bob):
    alice.balance = 5000
    bob.balance = 10
    
    winner = game.find_winner()
    assert winner == alice

@patch('moneypoly.game.Game.play_turn')
def test_run_loop_max_turns(mock_play, game):
    def fake_play_turn():
        game.turn_number += 1
        
    mock_play.side_effect = fake_play_turn

    game.turn_number = MAX_TURNS - 1
    game.run()
    mock_play.assert_called_once()