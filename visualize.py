import argparse

from simulation import Simulation
from strategy import Strategy
from game import Game

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", default="1", help="test's name to run")
    parser.add_argument("-s", "--strategy", action="store_false", help="turn AI off")
    args = parser.parse_args()

    path = f"tests/{args.test}.txt"
    strategy = Strategy() if args.strategy else None

    game = Game(Simulation.from_test_file(path), strategy)
    game.run()
