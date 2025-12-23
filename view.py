import pygame as pg

from core import State, Point
from simulation import Simulation


class Game:
    X_MIN = 0
    X_MAX = 15000
    Y_MIN = 0
    Y_MAX = 10000
    WIDTH = X_MAX - X_MIN
    HEIGHT = Y_MAX - Y_MIN

    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = (SCREEN_WIDTH * HEIGHT) // WIDTH
    FPS = 10

    def __init__(self, sim: Simulation):
        self.sim = sim

        pg.init()
        self.screen = pg.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

    def __del__(self):
        pg.quit()

    def get_screen_point(self, point: Point) -> tuple[int, int]:
        x, y = point
        x = ((x - Game.X_MIN) / Game.WIDTH) * Game.SCREEN_WIDTH
        y = ((y - Game.Y_MIN) / Game.HEIGHT) * Game.SCREEN_HEIGHT
        return x, y

    def render_state(self, s: State):
        self.screen.fill("black")
        
        car = self.sim.state.car
        cp = self.sim.current_cp
        print(car, cp)

        pg.draw.circle(self.screen, "white", self.get_screen_point(cp), 40)

        pg.draw.circle(self.screen, "red", self.get_screen_point(car), 10)

        pg.display.flip()

    def run(self):
        while True:
            dt = self.clock.tick(Game.FPS)
            self.render_state(self.sim.state)

            for e in pg.event.get():
                match e.type:
                    case pg.QUIT: return
                    case pg.KEYDOWN:
                        match e.key:
                            case pg.K_q: return


if __name__ == "__main__":
    game = Game(Simulation.from_test_file("tests/1"))
    game.run()
