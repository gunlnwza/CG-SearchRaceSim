import glob

from src.simulation import Simulation
from src.strategy import Strategy

if __name__ == "__main__":
    total_turns = 0

    for path in sorted(glob.glob("tests/*")):
        print(path, end=": ")
        try:
            sim = Simulation.from_test_file(path)
        except AssertionError:
            print("error parsing test file")
            break

        strategy = Strategy()
        turns = sim.run(strategy)
        total_turns += turns
        print(turns)
    print("\ntotal_turns:", total_turns)
