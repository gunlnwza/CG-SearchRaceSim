import math

from core import Car, Checkpoints, State, Action


def clamp(x, low, high):
    return min(max(low, x), high)


class Strategy:
    def __init__(self):
        self.checkpoints = None

    def read_checkpoints(self, checkpoints: Checkpoints):
        self.checkpoints = checkpoints

    def best_action(self, s: State) -> Action:
        car = s.car
        cp = self.checkpoints[s.cp_index]

        facing_vector = car.facing_vector
        dir_vector = cp - car
        angle_diff = math.degrees(facing_vector.angle_diff(dir_vector))
        r = clamp(round(angle_diff), -Action.MAX_ROTATION, Action.MAX_ROTATION)

        dist = car.dist_to(cp) * 0.05
        t = clamp(dist, 0, Action.MAX_THRUST)

        print(angle_diff, t)

        return Action(r, t)
