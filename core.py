import math


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
