from core import Car, Checkpoints, State, Action


class Strategy:
    def __init__(self):
        self.checkpoints = None

    def read_checkpoints(self, checkpoints: Checkpoints):
        self.checkpoints = checkpoints

    def best_action(self, s: State) -> Action:
        a = Action(0, 0)
        return a
