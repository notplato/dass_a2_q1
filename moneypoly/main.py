"""
Main entry point for the monopoly game.
"""

from moneypoly.game import Game


def get_player_names():
    """
    Gets the player names as inputs,
    and returns the the formatted player names.
    """
    print("Enter player names separated by commas (minimum 2 players):")
    raw = input("> ").strip()
    names = [n.strip() for n in raw.split(",") if n.strip()]
    return names


def main():
    """
    Entry point function of the whole game.
    """
    names = get_player_names()
    try:
        game = Game(names)
        game.run()
    except KeyboardInterrupt:
        print("\n\n  Game interrupted. Goodbye!")
    except ValueError as exc:
        print(f"Setup error: {exc}")


if __name__ == "__main__":
    main()
