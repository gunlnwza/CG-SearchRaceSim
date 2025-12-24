from typing import Optional
import math

from src.core import Action, Point, Checkpoint, Car
from src.simulation import Simulation
from src.strategy import Strategy

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame as pg


class Game:
    X_MIN = 0
    X_MAX = 16000
    Y_MIN = 0
    Y_MAX = 9000
    WIDTH = X_MAX - X_MIN
    HEIGHT = Y_MAX - Y_MIN

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = (SCREEN_WIDTH * HEIGHT) // WIDTH

    MAX_FPS = 21
    FPS = 11
    FPS_DIFF = 5

    def __init__(self, sim: Simulation, strategy: Optional[Strategy] = None):
        self.sim = sim

        self.strategy = strategy
        if self.strategy:
            self.strategy.read_checkpoints(sim.checkpoints)

        pg.init()
        pg.display.set_caption("Search Race")
        self.screen = pg.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

    def __del__(self):
        pg.quit()

    @classmethod
    def adjust_fps(cls, diff: int):
        if 0 < Game.FPS + diff <= Game.MAX_FPS:
            Game.FPS += diff

    def get_screen_point(self, point: Point) -> tuple[int, int]:
        x, y = point
        x = ((x - Game.X_MIN) * Game.SCREEN_WIDTH) // Game.WIDTH
        y = ((y - Game.Y_MIN) * Game.SCREEN_HEIGHT) // Game.HEIGHT
        return x, y

    def get_screen_length(self, length: int) -> float:
        res = (length * Game.SCREEN_WIDTH) // Game.WIDTH
        return res

    def _draw_cp(self, cp: Checkpoint, width=0):
        pg.draw.circle(self.screen, "white", self.get_screen_point(cp),
                       self.get_screen_length(cp.RADIUS), width)

    def _draw_car(self, car: Car):
        x, y = self.get_screen_point(car)
        pg.draw.circle(self.screen, "red", (x, y), 8)

        rad = math.radians(car.angle)
        x_end = x + 25 * math.cos(rad)
        y_end = y + 25 * math.sin(rad)
        pg.draw.line(self.screen, "red", (x, y), (x_end, y_end), 3)

    def render_state(self):
        car, cp = self.sim.car_and_cp()
        next_cp = self.sim.next_cp

        self.screen.fill("black")
        if cp:
            self._draw_cp(cp)
        if next_cp:
            self._draw_cp(next_cp, width=1)
        self._draw_car(car)
        pg.display.flip()

    def _get_human_action(self) -> Action:
        keys = pg.key.get_pressed()

        r = 0
        if keys[pg.K_a]:
            r -= Action.MAX_ROTATION
        if keys[pg.K_d]:
            r += Action.MAX_ROTATION

        t = 0
        if keys[pg.K_w]:
            t += Action.MAX_THRUST

        return Action(r, t)

    def get_action(self) -> Action:
        if self.strategy and self.sim.current_cp:
            return self.strategy.best_action(self.sim.state)
        return self._get_human_action()

    def run(self):
        self.render_state()
        while True:
            _ = self.clock.tick(Game.FPS)

            a = self.get_action()
            self.sim.step(a)
            self.render_state()

            for e in pg.event.get():
                match e.type:
                    case pg.QUIT: return
                    case pg.KEYDOWN:
                        match e.key:
                            case pg.K_q: return
                            case pg.K_LEFT: Game.adjust_fps(-Game.FPS_DIFF)
                            case pg.K_RIGHT: Game.adjust_fps(Game.FPS_DIFF)
