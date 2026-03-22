import pytest

from moneypoly.bank import Bank
from moneypoly.config import BANK_STARTING_FUNDS


# create stubs
class DummyPlayer:

    def __init__(self, name):
        self.name = name
        self.balance = 0

    def add_money(self, amount):
        self.balance += amount

# add fixtues for initalizing test state
@pytest.fixture
def bank():
    return Bank()

@pytest.fixture
def player():
    return DummyPlayer("test_player")

# test cases

def test_initial_state(bank):
    assert bank.get_balance() == BANK_STARTING_FUNDS
    assert bank._loans_issued == []
    assert bank._total_collected == 0

def test_normal_collect(bank):
    inital_funds = bank.get_balance()
    bank.collect(100)
    assert bank.get_balance() == inital_funds + 100
    assert bank._total_collected == 100

def test_negative_collect(bank):
    inital_funds = bank.get_balance()
    bank.collect(-100)
    assert bank.get_balance() == inital_funds

def test_zero_collect(bank):
    inital_funds = bank.get_balance()
    bank.collect(0)
    assert bank.get_balance() == inital_funds

def test_normal_payout(bank):
    inital_funds = bank.get_balance()
    amount_paid = bank.pay_out(100) # assuming inital funds have atleast 100

    assert amount_paid == 100
    assert bank.get_balance() == inital_funds - 100

def test_negative_payout(bank):
    inital_funds = bank.get_balance()
    amount_paid = bank.pay_out(-100) # assuming inital funds have atleast 100

    assert amount_paid == 0
    assert bank.get_balance() == inital_funds

def test_zero_payout(bank):
    inital_funds = bank.get_balance()
    amount_paid = bank.pay_out(0) # assuming inital funds have atleast 100

    assert amount_paid == 0
    assert bank.get_balance() == inital_funds

def test_extra_payout(bank):
    inital_funds = bank.get_balance()

    with pytest.raises(ValueError):
        bank.pay_out(inital_funds + 100)

def test_normal_give_loan(bank, player):
    initial_funds = bank.get_balance()
    bank.give_loan(player, 100) # assuming inital funds have atleast 100
    
    assert player.balance == 100
    assert bank.get_balance() == initial_funds - 100
    assert bank.total_loans_issued() == 100
    assert bank.loan_count() == 1

def test_negative_give_loan(bank, player):
    initial_funds = bank.get_balance()
    bank.give_loan(player, -100)
    
    assert player.balance == 0
    assert bank.get_balance() == initial_funds
    assert bank.total_loans_issued() == 0
    assert bank.loan_count() == 0 

def test_zero_give_loan(bank, player):
    initial_funds = bank.get_balance()
    bank.give_loan(player, 0)
    
    assert player.balance == 0
    assert bank.get_balance() == initial_funds
    assert bank.total_loans_issued() == 0
    assert bank.loan_count() == 0 

def test_extra_give_loan(bank, player):
    initial_funds = bank.get_balance()
    bank.give_loan(player, initial_funds + 100)
    
    assert player.balance == 0
    assert bank.get_balance() == initial_funds
    assert bank.total_loans_issued() == 0
    assert bank.loan_count() == 0