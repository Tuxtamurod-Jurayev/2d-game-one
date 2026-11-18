"""
Pixel Runner — 2D Game 01 (Master Roadmap)
Entry point to launch the game.
"""
import sys
from src.game import Game

def main():
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n[Game] Closed by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
