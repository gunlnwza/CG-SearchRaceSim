import math

from src.core import Checkpoints, State, Action


def clamp(x, low, high):
    return min(max(low, x), high)


class Strategy:
    def __init__(self):
        self.checkpoints = None

    def read_checkpoints(self, checkpoints: Checkpoints):
        self.checkpoints = checkpoints

    def best_action(self, s: State) -> Action:
        # loading vars
        car = s.car

        i = s.cp_index
        cp = self.checkpoints[i]
        next_cp = self.checkpoints[i + 1] if i + 1 < len(self.checkpoints) else None
        
        facing = car.facing_vector
        vel = car.vel_vector

        # ---
        # calculation

        dist = car.dist_to(cp)

        dir = (cp - car) - 2 * vel
        if next_cp:
            dir += 0.01 * (next_cp - cp)

        dir_norm = dir.norm()
        cosine = facing.dot(dir) / dir_norm if dir_norm > 0 else 0

        # ---
        # translating `facing` and `dir` to actions
        rotation = math.degrees(facing.angle(dir))
        thrust = (cosine if cosine > 0.70 else 0) * dist

        return Action(
            clamp(round(rotation), -Action.MAX_ROTATION, Action.MAX_ROTATION),
            clamp(round(thrust), 0, Action.MAX_THRUST)
        )
