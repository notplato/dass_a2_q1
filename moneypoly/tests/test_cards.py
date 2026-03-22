import pytest

from moneypoly.cards import CardDeck, CHANCE_CARDS, COMMUNITY_CHEST_CARDS

# fixtures for consistent test environment

@pytest.fixture
def chance_deck():
    return CardDeck(CHANCE_CARDS)

@pytest.fixture
def community_deck():
    return CardDeck(COMMUNITY_CHEST_CARDS)

# test cases

def test_inital_state(chance_deck, community_deck):
    assert chance_deck.cards == CHANCE_CARDS
    assert chance_deck.index == 0

    assert community_deck.cards == COMMUNITY_CHEST_CARDS
    assert community_deck.index == 0

def test_normal_draw(chance_deck):
    assert chance_deck.draw() == CHANCE_CARDS[0]
    assert chance_deck.index == 1

def test_cyclic_draw(chance_deck):
    inital_card = chance_deck.cards[0]
    for _ in range(len(CHANCE_CARDS)):
        chance_deck.draw()
    assert inital_card == chance_deck.draw()

def test_normal_peek(chance_deck):
    assert chance_deck.peek() == CHANCE_CARDS[0]
    assert chance_deck.index == 0

def test_shuffle(chance_deck):
    chance_deck.reshuffle()
    assert chance_deck.cards != CHANCE_CARDS
    assert chance_deck.index == 0

def test_count_remaining(chance_deck):
    for _ in range(3):
        chance_deck.draw()

    assert chance_deck.cards_remaining() == len(CHANCE_CARDS) - 3

def test_emtpy_deck_methods():
    empty_deck = CardDeck([])

    assert empty_deck.draw() is None
    assert empty_deck.peek() is None

    assert empty_deck.cards_remaining() == 0