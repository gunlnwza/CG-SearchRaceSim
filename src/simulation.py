from src.core import Car, Checkpoint, Checkpoints, State, Action
from src.strategy import Strategy


class Simulation:
    DEFAULT_MAX_TURNS = 600

    def __init__(self, car: Car, checkpoints: Checkpoints, *, max_turns=DEFAULT_MAX_TURNS):
        self.max_turns = max_turns
        self.checkpoints = checkpoints
        self.state = State(0, car)
        self.t = 0

    @classmethod
    def from_test_string(cls, test: str) -> "Simulation":
        checkpoints = []
        for i, line in enumerate(test.rstrip().split("\n")):
            try:
                match i:
                    case 0:
                        x, y, vx, vy, angle = map(int, line.split())
                        car = Car(x, y, vx, vy, angle)
                    case 1:
                        nb_checkpoints, laps = map(int, line.split())
                    case _:
                        x, y = map(int, line.split())
                        checkpoints.append(Checkpoint(x, y))
            except ValueError:
                raise AssertionError("test file string is wrong")

        checkpoints *= laps
        assert len(checkpoints) == nb_checkpoints * laps

        return Simulation(car, checkpoints)

    @classmethod
    def from_test_file(cls, path: str) -> "Simulation":
        with open(path) as f:
            return cls.from_test_string(f.read())

    @property
    def game_over(self):
        return self.state.cp_index >= len(self.checkpoints)

    @property
    def current_cp(self) -> Checkpoint | None:
        i = self.state.cp_index
        return self.cp(i) if i < len(self.checkpoints) else None

    @property
    def next_cp(self) -> Checkpoint | None:
        i = self.state.cp_index + 1
        return self.cp(i) if i < len(self.checkpoints) else None

    def cp(self, i: int) -> Checkpoint:
        return self.checkpoints[i]

    def car_and_cp(self):
        return self.state.car, self.current_cp

    def step(self, a: Action):
        if not self.game_over:  # advance time before processing action
            self.t += 1

        car, cp = self.car_and_cp()

        car.move(a)
        if cp and car in cp:
            self.state.cp_index += 1

    def run(self, strategy: Strategy) -> int | None:
        """Return the number of turns taken, None if does not finish in time"""
        strategy.read_checkpoints(self.checkpoints)
        while self.t <= self.max_turns:
            if self.game_over:
                return self.t
            a = strategy.best_action(self.state)
            self.step(a)
        return None
