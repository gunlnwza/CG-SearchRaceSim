import glob

from src.simulation import Simulation
from src.strategy import Strategy


def run_tests():
    """Return total_turns, None if error"""
    total_turns = 0
    for path in sorted(glob.glob("tests/*")):
        print(path, end=": ")
        try:
            sim = Simulation.from_test_file(path)
        except AssertionError:
            print("error parsing test file")
            return None

        strategy = Strategy()
        turns = sim.run(strategy)
        if not turns:
            print(f"took longer than {sim.max_turns} turns")
            return None

        print(turns)
        total_turns += turns

    return total_turns


if __name__ == "__main__":
    total_turns = run_tests()
    if total_turns:
        print("\ntotal_turns:", total_turns)
