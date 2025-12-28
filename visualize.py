import argparse
import sys
from pathlib import Path

from src.simulation import Simulation
from src.strategy import Strategy
from src.game import Game


def get_test_file(args):
    test: str = args.test
    if test.isdigit():
        test = test.rjust(2, "0")

    file = Path(f"tests/{test}")
    if not file.is_file():
        sys.exit(f"error opening {file}")

    return file


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("test", nargs="?", default="01", help="test's name to run")
    parser.add_argument("-s", "--strategy", action="store_false", help="turn AI off")
    args = parser.parse_args()

    test = get_test_file(args)

    sim = Simulation.from_test_file(test)
    strategy = Strategy() if args.strategy else None

    game = Game(sim, strategy)
    game.run()
