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

        facing = car.facing_vector
        vel = car.vel_vector

        # cancel out velocity, dir will now point to the place car need to actually be
        dir = (cp - car) - 2 * vel

        angle_diff = math.degrees(facing.angle_diff(dir))
        r = angle_diff

        dist = car.dist_to(cp)
        k = facing.dot(dir) / dir.norm() if dir.norm() > 0 else 0
        if k < 0.75:
            k = 0
        t = k * dist

        return Action(
            clamp(round(r), -Action.MAX_ROTATION, Action.MAX_ROTATION),
            clamp(round(t), 0, Action.MAX_THRUST)
        )
