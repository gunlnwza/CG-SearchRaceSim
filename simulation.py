import math

from strategy import Strategy


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def dist2_to(self, other: "Point") -> int:
        return (self.x - other.x)**2 + (self.y - other.y)**2

    def dist_to(self, other: "Point") -> float:
        return math.sqrt(self.dist2_to(other))


class Checkpoint(Point):
    def __init__(self, x, y):
        super().__init__(x, y)


Checkpoints = list[Checkpoint]


class Action:
    def __init__(self, rotation: int, thrust: int):
        self.rotation = rotation
        self.thrust = thrust
    
    def __post_init__(self):
        assert -15 <= self.rotation <= 15
        assert 0 <= self.thrust <= 200


class Car(Point):
    FRICTION = 0.85

    def __init__(self, x: int, y: int, vx: int, vy: int, angle: int):
        super().__init__(x, y)
        self.vx = vx
        self.vy = vy
        self.angle = angle

    def _rotate(self, rotation_angle: int):
        self.angle = (self.angle + rotation_angle) % 360

    def _accelerate(self, thrust: int):
        rad = math.radians(self.angle)
        ax = math.cos(rad) * thrust
        ay = math.sin(rad) * thrust
        self.vx += ax
        self.vy += ay

    def _displace(self):
        self.x = int(self.x + self.vx)
        self.y = int(self.y + self.vy)

    def _friction(self):
        self.vx = int(self.vx * Car.FRICTION)
        self.vy = int(self.vy * Car.FRICTION)

    def move(self, a: Action):
        self._rotate(a.rotation)
        self._accelerate(a.thrust)
        self._displace()
        self._friction()


class State:
    def __init__(self, cp_index: int, car: Car):
        self.cp_index = cp_index
        self.car = car


class Strategy:
    def __init__(self):
        self.checkpoints = None

    def read_checkpoints(self, checkpoints: Checkpoints):
        self.checkpoints = checkpoints

    def best_action(self, s: State) -> Action:
        a = Action(0, 0)
        return a


class Simulation:
    DEFAULT_MAX_TURNS = 600
    CHECKPOINT_RADIUS = 300

    def __init__(self, car: Car, checkpoints: Checkpoints, *, max_turns=DEFAULT_MAX_TURNS):
        self.max_turns = max_turns
        self.checkpoints = checkpoints
        self.state = State(0, car)

    @classmethod
    def from_test_string(cls, test: str) -> "Simulation":
        checkpoints = []
        for i, line in enumerate(test.rstrip().split("\n")):
            match i:
                case 0:
                    x, y, vx, vy, angle = map(int, line.split())
                    car = Car(x, y, vx, vy, angle)
                case 1:
                    n = int(line)
                case _:
                    x, y = map(int, line.split())
                    checkpoints.append(Checkpoint(x, y))
        assert len(checkpoints) == n
        return Simulation(car, checkpoints)

    @classmethod
    def from_test_file(cls, path: str) -> "Simulation":
        with open(path) as f:
            return cls.from_test_string(f.read())

    @property
    def game_over(self):
        return self.state.cp_index >= len(self.checkpoints)

    def update(self, a: Action):
        car = self.state.car
        current_cp = self.checkpoints[self.state.cp_index]

        car.move(a)
        if car.dist_to(current_cp) <= Simulation.CHECKPOINT_RADIUS:
            self.state.cp_index += 1

    def run(self, strategy: Strategy) -> bool:
        strategy.read_checkpoints(self.checkpoints)
        for _ in range(self.max_turns):
            a = strategy.best_action(self.state)
            self.update(a)
            if self.game_over:
                return True
        return False


if __name__ == "__main__":
    sim = Simulation.from_test_file("tests/test_1.txt")
    s = Strategy()
    res = sim.run(s)
    print("OK" if res else "KO")
