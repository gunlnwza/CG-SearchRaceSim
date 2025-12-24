import sys
import math
from dataclasses import dataclass
from typing import Optional
import heapq
import time


@dataclass
class Checkpoint:
    x: int
    y: int

    @property
    def point(self):
        return (self.x, self.y)


@dataclass
class Car:
    x: float
    y: float
    vx: float
    vy: float
    angle: int

    def __repr__(self):
        return f"Car(pos=({self.x}, {self.y}), vel=({self.vx}, {self.vy}), angle={self.angle})"

    @property
    def point(self):
        return (self.x, self.y)

    def copy(self) -> "Car":
        return Car(self.x, self.y, self.vx, self.vy, self.angle)

    def _rotate(self, rotation_angle):
        self.angle = (self.angle + rotation_angle) % 360

    def _accelerate(self, thrust):
        rad = math.radians(self.angle)
        ax = math.cos(rad) * thrust
        ay = math.sin(rad) * thrust
        self.vx += ax
        self.vy += ay

    def _move(self):
        self.x = int(self.x + self.vx)
        self.y = int(self.y + self.vy)

    def _friction(self, f=0.85):
        self.vx = int(self.vx * f)
        self.vy = int(self.vy * f)

    def drive(self, rotation_angle: int, thrust: int):
        self._rotate(rotation_angle)
        self._accelerate(thrust)
        self._move()
        self._friction()


@dataclass
class State:
    checkpoints: list[Checkpoint]  # reference to a list of checkpoints
    cp_idx: int
    car: Car

    def __repr__(self):
        return f"State(cp_idx={self.cp_idx}, {self.car})"

    @property
    def goal(self):
        return self.checkpoints[self.cp_idx]


@dataclass
class Action:
    rotation_angle: int
    thrust: int

    def __repr__(self):
        return f"Action({self.rotation_angle}, {self.thrust})"


@dataclass
class Node:
    state: State
    parent: Optional["Node"]
    action: Optional[Action]
    depth: int = 0

    def cost(self) -> float:
        return math.dist(self.state.goal.point, self.state.car.point)

    def __lt__(self, other: "Node"):
        return self.cost() < other.cost()


def debug(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr, flush=True)


MAX_DEPTH = 3
ROTATION_ANGLES = (-18, -6, 0, 6, 18)
THRUSTS = (0, 100, 200)
ACTIONS = [Action(a, t) for a in ROTATION_ANGLES for t in THRUSTS]


def find_best_action(state: State, max_time: float = 0.050) -> Optional[Action]:
    global g_message

    time_start = time.perf_counter()
    checkpoints = state.checkpoints

    best_node = Node(state, None, None)
    pq = [best_node]
    while time.perf_counter() - time_start < max_time and pq:
        node = heapq.heappop(pq)

        for action in ACTIONS:
            next_car = node.state.car.copy()
            next_car.drive(action.rotation_angle, action.thrust)

            next_state = State(checkpoints, node.state.cp_idx, next_car)  # TODO: check collision with goal to update cp_idx
            next_node = Node(next_state, node, action, node.depth + 1)

            if next_node < best_node:
                best_node = next_node
            if next_node.depth < MAX_DEPTH:
                heapq.heappush(pq, next_node)

    g_message = ""
    if not pq:
        g_message = "ALL SEARCHED"

    while best_node.depth > 1:
        best_node = best_node.parent
    return best_node.action


g_message = ""


# Response time for the first turn ≤ 1000 ms
# Response time per turn ≤ 50 ms
# TODO: iterative deepening pls
def main():
    global g_message

    # Read checkpoints
    checkpoints: list[Checkpoint] = []
    n = int(input())
    for _ in range(n):
        x, y = map(int, input().split())
        checkpoints.append(Checkpoint(x, y))

    # Game loop
    MAX_TURNS = 600
    for _ in range(MAX_TURNS):
        # Read state
        cp_idx, x, y, vx, vy, angle = map(int, input().split())
        state = State(checkpoints, cp_idx, Car(x, y, vx, vy, angle))

        # x y thrust message | EXPERT rotationAngle thrust message
        action = find_best_action(state)
        if action:
            print(f"EXPERT {action.rotation_angle} {action.thrust} {g_message}")
        else:
            # It can happen that the goal is behind,
            # and the AI cannot distinguish what action is best.
            # (As per the cost function, driving forward only increase the cost)
            # Resulting in not knowing what to do.
            x, y = state.goal.point
            g_message = "COURSE CORRECTING"
            print(f"{x} {y} 0 {g_message}")


if __name__ == "__main__":
    main()
