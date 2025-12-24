from dataclasses import dataclass
from typing import ClassVar
import math


@dataclass
class Point:
    x: int
    y: int

    def __iter__(self):
        yield self.x
        yield self.y

    def dist2_to(self, other: "Point") -> int:
        return (self.x - other.x)**2 + (self.y - other.y)**2

    def dist_to(self, other: "Point") -> float:
        return math.sqrt(self.dist2_to(other))

    def __add__(self, other: "Point") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)


@dataclass
class Vector(Point):
    def norm2(self):
        return self.x**2 + self.y**2

    def norm(self):
        return math.sqrt(self.norm2())

    def dot(self, other: "Vector") -> float:
        return self.x * other.x + self.y * other.y
    
    def cross(self, other: "Vector") -> float:
        return self.x * other.y - self.y * other.x
    
    def _norm_pair(self, other: "Vector") -> float:
        a2 = self.norm2()
        b2 = other.norm2()
        if a2 == 0 or b2 == 0:
            return None
        return math.sqrt(a2 * b2)

    def cos_angle(self, other: "Vector") -> float:
        den = self._norm_pair(other)
        if not den:
            return 0
        return self.dot(other) / den
    
    def sin_angle(self, other: "Vector") -> float:
        den = self._norm_pair(other)
        if not den:
            return 0
        return self.cross(other) / den

    def angle(self, other: "Vector") -> float:
        """Return in radians"""
        return math.atan2(self.cross(other), self.dot(other))

    def __mul__(self, other: int | float) -> "Vector":
        return Vector(other * self.x, other * self.y)

    def __rmul__(self, other: int | float) -> "Vector":
        return self.__mul__(other)


@dataclass
class Action:
    MAX_ROTATION: ClassVar[int] = 18
    MAX_THRUST: ClassVar[int] = 200

    rotation: int
    thrust: int

    def __post_init__(self):
        assert -Action.MAX_ROTATION <= self.rotation <= Action.MAX_ROTATION
        assert 0 <= self.thrust <= Action.MAX_THRUST


class Car(Point):
    FRICTION = 0.85

    def __init__(self, x: int, y: int, vx: int, vy: int, angle: int):
        super().__init__(x, y)
        self.vx = vx
        self.vy = vy
        self.angle = angle

    @property
    def facing_vector(self) -> Vector:
        rad = math.radians(self.angle)
        return Vector(math.cos(rad), math.sin(rad))

    @property
    def vel_vector(self) -> Vector:
        return Vector(self.vx, self.vy)

    def __repr__(self):
        return f"Car(({self.x}, {self.y}), ({self.vx}, {self.vy}), {self.angle})"

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


class Checkpoint(Point):
    RADIUS = 600
    RADIUS2 = RADIUS ** 2

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def __repr__(self):
        return f"Checkpoint(({self.x}, {self.y}))"
    
    def contain(self, other: Point):
        return self.dist2_to(other) < Checkpoint.RADIUS2

    def __contains__(self, other: Point):
        return self.contain(other)


Checkpoints = list[Checkpoint]


@dataclass
class State:
    cp_index: int
    car: Car
