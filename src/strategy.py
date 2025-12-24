import math

from src.core import Checkpoint, Checkpoints, State, Action, Vector, Car


def clamp(x, low, high):
    return min(max(low, x), high)


class Strategy:
    def __init__(self):
        self.checkpoints = None

    def read_checkpoints(self, checkpoints: Checkpoints):
        self.checkpoints = checkpoints

    def turns_to_reach(self, car: Car, cp: Checkpoint, max_turns=100) -> int | None:
        """
        extrapolate position and velocity, estimate how long until goal
        return None if too long
        """
        pos = Vector(car.x, car.y)
        vel = car.vel_vector

        min_dist2 = 1e9
        for t in range(max_turns + 1):
            pos += vel
            dist2 = cp.dist2_to(pos)
            if dist2 < cp.RADIUS2:
                return t
            if dist2 > min_dist2:
                break
            min_dist2 = dist2

        return None

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
        dir = cp - car
        dist = dir.norm()

        if next_cp:
            change_target_bound = 3
            turns = self.turns_to_reach(car, cp, change_target_bound)
            if turns and turns <= change_target_bound:
                a = 0.80
                dir = a * dir + (1 - a) * (next_cp - car)

        dir -= 4 * vel
        cosine = facing.cos_angle(dir)
 
        # ---
        # translating intents into actions
        rotation = math.degrees(facing.angle(dir))
        thrust = (cosine if cosine >= 0.6 else 0) * dist

        return Action(
            clamp(round(rotation), -Action.MAX_ROTATION, Action.MAX_ROTATION),
            clamp(round(thrust), 0, Action.MAX_THRUST)
        )
