import pytest

from moneypoly.property import Property, PropertyGroup

# --- STUBS & FIXTURES ---

class DummyPlayer:
    def __init__(self, name):
        self.name = name

@pytest.fixture
def player():
    return DummyPlayer("Player1")

@pytest.fixture
def player2():
    return DummyPlayer("Player2")

@pytest.fixture
def group():
    return PropertyGroup("Brown", "brown")

@pytest.fixture
def stats():
    return {"price": 60, "base_rent": 2}

@pytest.fixture
def prop(stats):
    return Property("Baltic Ave", 1, stats)

def test_property_initialization_no_group(prop, stats):
    assert prop.name == "Baltic Ave"
    assert prop.position == 1
    assert prop.stats["price"] == 60
    assert prop.stats["base_rent"] == 2
    assert prop.stats["mortgage_value"] == 30
    assert prop.owner is None
    assert prop.group is None
    assert prop.is_mortgaged is False

def test_property_initialization_with_group(stats, group):
    new_prop = Property("Mediteranean Ave", 3, stats, group=group)
    assert new_prop.group == group
    assert new_prop in group.properties

def test_get_rent_mortgaged_branch(prop):
    prop.is_mortgaged = True
    assert prop.get_rent() == 0

def test_get_rent_double_rent(stats, group, player):
    prop1 = Property("Prop 1", 1, stats, group=group)
    prop2 = Property("Prop 2", 2, stats, group=group)
    
    prop1.owner = player
    
    assert prop1.get_rent() == 2

def test_get_rent_standard_branch(prop, player):
    prop.owner = player
    assert prop.get_rent() == prop.stats["base_rent"]

def test_mortgage_standard_branch(prop):
    payout = prop.mortgage()
    assert payout == 30
    assert prop.is_mortgaged is True

def test_mortgage_already_mortgaged_branch(prop):
    prop.mortgage()
    payout = prop.mortgage()
    assert payout == 0

def test_unmortgage_standard_branch(prop):
    prop.mortgage()
    cost = prop.unmortgage()
    
    assert cost == 33
    assert prop.is_mortgaged is False

def test_unmortgage_not_mortgaged_branch(prop):
    cost = prop.unmortgage()
    assert cost == 0

def test_is_available_true_path(prop):
    assert prop.is_available() is True

def test_is_available_false_owned_path(prop, player):
    prop.owner = player
    assert prop.is_available() is False

def test_is_available_false_mortgaged_path(prop):
    prop.is_mortgaged = True
    assert prop.is_available() is False

def test_group_initialization(group):
    assert group.name == "Brown"
    assert group.color == "brown"
    assert group.properties == []

def test_group_add_property_new_branch(group, prop):
    group.add_property(prop)
    assert prop in group.properties
    assert prop.group == group

def test_group_add_property_duplicate_branch(group, prop):
    group.add_property(prop)
    group.add_property(prop)
    assert group.size() == 1

def test_group_all_owned_by_bug_path(group, stats, player, player2):
    prop1 = Property("Prop 1", 1, stats, group=group)
    prop2 = Property("Prop 2", 2, stats, group=group)
    
    prop1.owner = player
    prop2.owner = player2
    
    assert group.all_owned_by(player) is False

def test_group_all_owned_by_true_path(group, stats, player):
    prop1 = Property("Prop 1", 1, stats, group=group)
    prop2 = Property("Prop 2", 2, stats, group=group)
    
    prop1.owner = player
    prop2.owner = player
    
    assert group.all_owned_by(player) is True

def test_group_all_owned_by_none_player_branch(group):
    assert group.all_owned_by(None) is False

def test_group_get_owner_counts(group, stats, player, player2):
    prop1 = Property("Prop 1", 1, stats, group=group)
    prop2 = Property("Prop 2", 2, stats, group=group)
    Property("Prop 3", 3, stats, group=group) # Unowned
    
    prop1.owner = player
    prop2.owner = player2
    
    counts = group.get_owner_counts()
    assert counts[player] == 1
    assert counts[player2] == 1
    assert None not in counts

def test_group_size(group, prop):
    group.add_property(prop)
    assert group.size() == 1