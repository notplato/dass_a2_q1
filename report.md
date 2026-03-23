## Design and Analysis of Software Systems: Assignment 2
## Part 1: White Box Testing

### 1.3

#### _bank.py_

`test_initial_state()`:
Purpose: Test the initialization.

`test_normal_collect()`:
* **Purpose**: Test the standard (positive collect value) collection execution path.

`test_negative_collect()`:
* **Purpose**: Test the collection workflow with negative collect value.

* **Bug found**: Negative values for collect are not ignored.

`test_zero_collect()`:
* **Purpose**: Test the collection workflow with zero collect value.

`test_normal_payout()`:
* **Purpose**: Test the standard (positive and reasonable payout value) payout workflow.

`test_negative_payout()`:
* **Purpose**: Test the payout workflow with negative payout value.

`test_zero_payout()`:
* **Purpose**: Test the payout workflow with zero payout value.

`test_extra_payout()`:
* **Purpose**: Test the payout workflow with payout value > available funds.

`test_normal_give_loan()`:
* **Purpose** : Test the standard (positive and reasonable loan value) loan workflow.

* **Bug found**: Loan values are not deducted from the bank's funds.

`test_negative_give_loan()`:
* **Purpose**: Test the loan workflow with negative loan value.

* **Bug found**: Negative loan values are not ignored.

`test_zero_give_loan()`:
* **Purpose**: Test the loan workflow with zero loan value.

`test_extra_give_loan()`:
* **Purpose**: Test the loan workflow with loan value > available funds.

* **Bug found**: Loans with amount greater than available balance were not ignored.

#### _board.py_

`test_board_initialization()`:
* **Purpose:** To verify that the constructor correctly instantiates the standard 8 colour groups and 22 street properties.

`test_get_property_at_valid_branch()`:
* **Purpose:** To test the successful execution path where a valid property position correctly returns the matching `Property` object.

`test_get_property_at_invalid_branch()`:
* **Purpose:** To test the fallback execution path returning `None` if an invalid or non-property position is queried.

`test_get_tile_type_special_branch()`:
* **Purpose:** To test the `if position in SPECIAL_TILES:` branch, verifying it maps correctly to spaces like "Go" and the Tax tiles.

`test_get_tile_type_property_branch()`:
* **Purpose:** To test the `if self.get_property_at(position) is not None:` branch, verifying it identifies standard purchasable spaces.

`test_get_tile_type_blank_branch()`:
* **Purpose:** To test the fallback execution path. Unassigned spaces (like position 12) correctly evaluate to `"blank"`.

`test_is_purchasable_true_path()`:
* **Purpose:** To test the execution path where an unowned, unmortgaged property evaluates to `True`.

`test_is_purchasable_not_property_branch()`:
* **Purpose:** To test the `if prop is None:` error-handling branch, ensuring players cannot attempt to purchase spaces like "Go".

`test_is_purchasable_railroad()`:
* **Purpose:** To test the purchasable logic on Railroad tiles.
* **Bug found:** The test exposes a critical logic gap. Railroads are defined purely as strings inside `SPECIAL_TILES` but are not instantiated as `Property` objects. Consequently, `get_property_at()` returns `None`, which triggers the `is_purchasable()` method to return `False`. Railroads are entirely un-buyable in the current game state.

`test_is_purchasable_mortgaged_branch()`:
* **Purpose:** To test the `if prop.is_mortgaged is True:` branch, ensuring players cannot buy mortgaged properties from the bank.

`test_is_purchasable_owned_branch()`:
* **Purpose:** To test the implicit `return prop.owner is None` branch, ensuring owned properties return `False`.

`test_is_special_tile_true()`:
* **Purpose:** To verify the boolean logic returns `True` for config-mapped special tiles.

`test_is_special_tile_false()`:
* **Purpose:** To verify the boolean logic returns `False` for standard properties.

`test_properties_owned_by()`:
* **Purpose:** To verify the list comprehension effectively filters the properties array by a specific `owner`.

`test_unowned_properties()`:
* **Purpose:** To verify the list comprehension effectively filters the properties array for `None` values.

#### _cards.py_

`test_initial_state()`:
* **Purpose:** To verify that the `CardDeck` constructor correctly initializes the internal `cards` array with the provided data and sets the starting draw `index` to 0.

`test_normal_draw()`:
* **Purpose:** To test the standard execution path of the `draw()` method, ensuring it successfully returns the top card and correctly increments the internal index tracker.

`test_cyclic_draw()`:
* **Purpose:** To test the modulo wrapping boundary logic. By drawing more cards than the deck contains, it verifies that the deck correctly loops back to the beginning without throwing an `IndexError`.

`test_normal_peek()`:
* **Purpose:** To verify that the `peek()` method correctly returns the upcoming card without mutating the deck's state or advancing the internal index.

`test_shuffle()`:
* **Purpose:** To test the execution path of the `reshuffle()` method, ensuring the internal deck array is randomized and the draw index is properly reset back to 0.

`test_count_remaining()`:
* **Purpose:** To verify the mathematical calculation inside `cards_remaining()`, ensuring it accurately reports the difference between the total deck size and the current modulo index.

`test_empty_deck_methods()`:
* **Purpose:** To verify the error-handling branches when a deck is instantiated with zero cards. It checks that `draw()`, `peek()`, and `cards_remaining()` handle the empty state gracefully.
* **Bug found:** The test exposes a fatal logic error in the `cards_remaining()` method. While `draw` and `peek` explicitly check for an empty deck, `cards_remaining` blindly executes `(self.index % len(self.cards))`. When the deck is empty, its length is `0`, causing Python to throw a `ZeroDivisionError` and crash the entire program.

#### _dice.py_

`test_initial_state()`:
* **Purpose:** To verify that the constructor properly initializes the dice faces and the doubles streak to zero.

`test_reset()`:
* **Purpose:** To verify that the `reset()` method correctly wipes out the dice faces and the streak back to zero after the state has been manually altered.

`test_roll_doubles_branch()`:
* **Purpose:** Uses mocking to bypass randomness and test the specific logical branch where consecutive doubles are rolled, ensuring the `doubles_streak` counter correctly increments.

`test_roll_non_doubles_branch()`:
* **Purpose:** Uses mocking to test the `else` branch of the `roll()` method, ensuring that rolling non-doubles successfully resets a previous `doubles_streak` back to 0.

`test_is_doubles_true_path()`:
* **Purpose:** To test the execution path of the `is_doubles()` helper method when both dice values match.

`test_is_doubles_false_path()`:
* **Purpose:** To test the execution path of the `is_doubles()` helper method when the dice values differ.

`test_total_calculation()`:
* **Purpose:** To verify the mathematical addition logic within the `total()` helper method.

`test_describe_doubles_branch()`:
* **Purpose:** To test the string formatting branch in `describe()` when a valid doubles roll has occurred.

`test_describe_non_doubles_branch()`:
* **Purpose:** To test the standard string formatting branch in `describe()` when a normal, non-doubles roll has occurred.

`test_doubles_initial_state()`:
* **Purpose:** To test the edge case where the dice state is evaluated or described before any rolls have actually occurred.
* **Bug found:** Because initialization sets both dice to `0`, the original `is_doubles()` method evaluates to `True` (since 0 == 0), causing `describe()` to incorrectly report "0 + 0 = 0 (DOUBLES)" instead of properly handling the unrolled state.

`test_six_sides()`:
* **Purpose:** A Monte Carlo style boundary test to ensure the dice can successfully hit the maximum expected upper bound of a standard die (6).
* **Bug found:** The `roll()` method incorrectly uses `random.randint(1, 5)`. Because `randint` is inclusive, it is mathematically impossible for the simulation to ever roll a 6, bounding the maximum dice total to 10 instead of 12.

#### _game.py_

`test_game_initialization()`:
* **Purpose:** To verify the `Game` constructor properly instantiates all sub-modules (Board, Bank, Dice, Players) and initial turn trackers.

`test_current_player()`:
* **Purpose:** To verify the helper method accurately accesses the `players` array using the dynamic `current_index`.

`test_advance_turn()`:
* **Purpose:** To verify the modulo math logic safely wraps the `current_index` back to 0 after the last player's turn.

`test_play_turn_in_jail()`:
* **Purpose:** To verify that if a player starts their turn with `in_jail == True`, the game correctly routes them to `_handle_jail_turn` and bypasses standard movement.

`test_play_turn_standard()`:
* **Purpose:** To test the standard execution path of a turn (rolling the dice and resolving movement).

`test_play_turn_doubles_extra_roll()`:
* **Purpose:** To verify the `if self.state["dice"].is_doubles():` branch grants the player an extra turn without advancing the `current_index`.

`test_play_turn_speeding_jail()`:
* **Purpose:** To verify that rolling three consecutive doubles immediately halts the player's turn and routes them to Jail.

`test_resolve_go_to_jail()`:
* **Purpose:** To verify the explicit tile routing branch that forces a player's position to `JAIL_POSITION`.

`test_resolve_income_tax()` & `test_resolve_luxury_tax()`:
* **Purpose:** To test the specific tax branches inside `_move_and_resolve()`, ensuring the correct static amounts are deducted.

`test_resolve_free_parking()`:
* **Purpose:** To verify the empty execution path where resting on Free Parking safely does nothing.

`test_resolve_chance_and_community_chest()`:
* **Purpose:** To verify that landing on card tiles successfully triggers the deck draw and routes to `_apply_card()`.

`test_resolve_property_and_railroad()`:
* **Purpose:** To verify that standard real estate spaces correctly pass the property object to `_handle_property_tile()`.

`test_handle_unowned_buy()`, `test_handle_unowned_auction()`, `test_handle_unowned_skip()`:
* **Purpose:** Uses mocked input to test the interactive menu routing, verifying that the console commands 'b', 'a', and 's' trigger their respective game functions.

`test_handle_owned_by_self()` & `test_handle_owned_by_other()`:
* **Purpose:** To verify the branching logic that either allows a player to rest safely on their own property, or forces them to pay rent to an opponent.

`test_buy_property_success_branch()` & `test_buy_property_insufficient_funds_branch()`:
* **Purpose:** To test standard property purchasing, validating both the successful transaction and the `if player.balance <= prop.price:` boundary condition.

`test_pay_rent()`:
* **Purpose:** To the symmetrical deduction and addition of rent funds between two players.
* **Bug found:** The logic executes `player.deduct_money(rent)` but entirely omits the step of adding those funds to `prop.owner`.

`test_pay_rent_mortgaged_branch()`:
* **Purpose:** To verify the branch where mortgaged properties successfully bypass rent calculations.

`test_mortgage_and_unmortgage_flow()`:
* **Purpose:** To verify the logic between `mortgage_property()` and `unmortgage_property()`, ensuring boolean flags toggle correctly and the 10% interest penalty is applied.

`test_mortgage_wrong_owner()` & `test_mortgage_remortgage()`:
* **Purpose:** To verify the error-handling branches preventing players from mortgaging properties they don't own or that are already mortgaged.

`test_trade()`:
* **Purpose:** To test the symmetrical exchange of assets and cash in a player-to-player trade.
* **Bug found:** Similar to the rent bug, the trade logic deducts cash from the buyer but fails to call `seller.add_money()`. The cash payment vanishes into the void.

`test_trade_wrong_owner()` & `test_trade_insufficient_funds()`:
* **Purpose:** To verify the error-handling boundaries protecting trade operations from invalid states.

`test_auction_all_pass_branch()`, `test_auction_bid_too_low_branch()`, `test_auction_cannot_afford_branch()`, `test_auction_valid_bidding_and_winner_branch()`:
* **Purpose:** To verify the internal boundary checks of the auction block, ensuring bids are strictly validated against minimum increments and player wallets before ownership is awarded.

`test_jail_use_card()`, `test_jail_pay_fine()`, `test_jail_serve_time()`, `test_jail_mandatory_release()`:
* **Purpose:** To verify the four distinct logical paths a player can take while incarcerated, ensuring turn counters, boolean states, and fine deductions update accurately.

`test_apply_card_collect()`, `test_apply_card_pay()`, `test_apply_card_jail()`, `test_apply_card_jail_free()`, `test_apply_card_move_to_pass_go()`, `test_apply_card_collect_from_all()`:
* **Purpose:** To systematically verify the dictionary-based switchboard inside `_apply_card()`, ensuring every possible card action correctly mutates player and board state.

`test_check_bankruptcy()`:
* **Purpose:** To verify the state-cleanup branch inside `_check_bankruptcy()`. It confirms the player is flagged, removed from the active list, and all properties are successfully decoupled and returned to the bank.

`test_find_winner()`:
* **Purpose:** To test the lambda logic which identifies the highest net-worth player.
* **Bug found:** The developer utilized Python's built-in `min()` function rather than `max()`. The system incorrectly declares the poorest player in the game as the winner.

`test_run_loop_max_turns()`:
* **Purpose:** To verify the `while` loop boundary condition `self.turn_number < MAX_TURNS` safely halts the game.

#### _player.py_

`test_initialization_default()`:
* **Purpose:** To verify that the default constructor properly assigns starting variables, including the `STARTING_BALANCE` config.

`test_initialization_custom()`:
* **Purpose:** To test the alternate branch of the constructor where a custom starting balance is passed as an argument.

`test_add_money_valid_branch()`:
* **Purpose:** To test the standard execution path of `add_money()` when a positive integer is provided.

`test_add_money_negative_branch()`:
* **Purpose:** To test the error-handling branch of `add_money()`, ensuring a `ValueError` is raised if a negative input is passed.

`test_deduct_money_valid_branch()`:
* **Purpose:** To test the standard execution path of `deduct_money()` when a positive integer is provided.

`test_deduct_money_negative_branch()`:
* **Purpose:** To test the error-handling branch of `deduct_money()`, ensuring a `ValueError` is raised if a negative input is passed.

`test_is_bankrupt_true_path()`:
* **Purpose:** To verify the `is_bankrupt()` boolean logic evaluates to `True` when balance drops to zero or goes negative.

`test_is_bankrupt_false_path()`:
* **Purpose:** To verify the `is_bankrupt()` boolean logic evaluates to `False` when the player still has a positive balance.

`test_net_worth_incomplete_bug()`:
* **Purpose:** To verify the `net_worth()` calculation logic.
* **Bug found:** The docstring dictates it calculates "total net worth," but the logic solely returns the cash `balance`, completely failing to account for the value of the assets stored in the `properties` array.

`test_move_lands_exactly_on_go_branch()`:
* **Purpose:** To test the specific positional branch where `(position + steps) % BOARD_SIZE` resolves exactly to `0`, ensuring the `GO_SALARY` is correctly awarded.

`test_move_passes_go_bug()`:
* **Purpose:** To test the edge case of board wrap-around where a player's starting position plus steps results in a new position greater than 0.
* **Bug found:** The `move()` function's docstring claims it pays the player if they "pass or land on" Go. However, the logic branch `if self.position == 0:` only triggers if they land *exactly* on the Go square. Players wrapping around the board to position 1 or higher are incorrectly denied their salary.

`test_go_to_jail()`:
* **Purpose:** To test the state transition when a player is sent to jail, ensuring position, jail boolean, and turn counters update simultaneously.

`test_add_property_new_branch()`:
* **Purpose:** To test the standard execution path of acquiring a new property tile.

`test_add_property_duplicate_branch()`:
* **Purpose:** To test the branch `if prop not in self.properties:` to ensure the game silently prevents adding identical duplicate properties to a single player.

`test_remove_property_existing_branch()`:
* **Purpose:** To test the standard execution path of removing/selling an owned property tile.

`test_remove_property_nonexistent_branch()`:
* **Purpose:** To test the `if prop in self.properties:` branch to ensure the game handles attempts to remove unowned properties gracefully without crashing.

#### _property.py_

`test_property_initialization_no_group()`:
* **Purpose:** To verify standard initialization of the `Property` class when no `group` argument is passed, checking that the `mortgage_value` calculation logic applies correctly.

`test_property_initialization_with_group()`:
* **Purpose:** To verify the branch in the constructor where a `PropertyGroup` is passed, ensuring the property correctly links itself to the group's internal list.

`test_get_rent_mortgaged_branch()`:
* **Purpose:** To test the specific `if self.is_mortgaged:` branch of `get_rent()`, ensuring mortgaged properties successfully return `$0`.

`test_get_rent_double_rent()`:
* **Purpose:** To test the `all_owned_by` logical branch within `get_rent()` when a player holds a partial monopoly. 
* **Bug found:** The test exposes a cascading failure caused by the `PropertyGroup`. Because the group incorrectly validates monopolies, a player who owns only 1 out of 2 properties in a group will improperly trigger the `FULL_GROUP_MULTIPLIER`, charging opponents double rent.

`test_get_rent_standard_branch()`:
* **Purpose:** To test the fallback execution path of `get_rent()` where the property simply returns its `base_rent`.

`test_mortgage_standard_branch()`:
* **Purpose:** To test the primary execution path of the `mortgage()` method, verifying the boolean state changes to `True` and the proper value is returned.

`test_mortgage_already_mortgaged_branch()`:
* **Purpose:** To test the `if self.is_mortgaged:` branch to prevent double-mortgaging and ensure it returns 0.

`test_unmortgage_standard_branch()`:
* **Purpose:** To test the primary execution path of `unmortgage()`, verifying that the 10% interest rate is calculated and cast to an integer correctly.

`test_unmortgage_not_mortgaged_branch()`:
* **Purpose:** To test the `if not self.is_mortgaged:` branch to prevent unmortgaging a free property.

`test_is_available_true_path()`:
* **Purpose:** To test the execution path where `is_available()` correctly evaluates to `True` (unowned and unmortgaged).

`test_is_available_false_owned_path()`:
* **Purpose:** To test the path where an existing owner causes `is_available()` to evaluate to `False`.

`test_is_available_false_mortgaged_path()`:
* **Purpose:** To test the path where an active mortgage causes `is_available()` to evaluate to `False`.

`test_group_initialization()`:
* **Purpose:** To verify the `PropertyGroup` constructor initializes correctly.

`test_group_add_property_new_branch()`:
* **Purpose:** To test the execution path of adding a distinct `Property` to the group's array.

`test_group_add_property_duplicate_branch()`:
* **Purpose:** To test the explicit `if prop not in self.properties:` branch to ensure identical instances cannot be added multiple times.

`test_group_all_owned_by_bug_path()`:
* **Purpose:** To assert the strict boolean requirement for monopoly ownership.
* **Bug found:** The `all_owned_by()` logic iterates through properties using the `any()` function rather than `all()`. This means if a player owns even a single property out of a group of three, the game legally considers them to own the entire monopoly.

`test_group_all_owned_by_true_path()`:
* **Purpose:** To test the execution path where the player genuinely does own every property in the group.

`test_group_all_owned_by_none_player_branch()`:
* **Purpose:** To test the explicit error-handling branch `if player is None:`, ensuring unowned groups don't accidentally register as monopolies.

`test_group_get_owner_counts()`:
* **Purpose:** To verify the loop execution path in `get_owner_counts()`, ensuring the dictionary correctly aggregates property counts per player while ignoring unowned properties.

`test_group_size()`:
* **Purpose:** To verify the `size()` helper method returns the accurate length of the properties array.

#### _ui.py_

`test_format_currency()`:
* **Purpose:** To verify the static string injection and thousand-separator formatting (`:,`).

`test_safe_int_input_valid()`:
* **Purpose:** Uses mocked input to test the standard `try:` execution path, successfully capturing and casting a string integer to an `int` type.

`test_safe_int_input_invalid_branch()`:
* **Purpose:** To test the `except ValueError:` error-handling branch, ensuring that un-castable string inputs (like letters) are safely caught and the fallback `default` variable is returned without crashing the program.

`test_confirm_true_branch()`:
* **Purpose:** To test the explicit input sanitization logic (`.strip().lower() == "y"`). Verifies that a messy string like `"  Y  "` successfully evaluates to `True`.

`test_confirm_false_branch()`:
* **Purpose:** To test standard boolean fallbacks, proving that any input other than a strict 'y' evaluates to `False`.