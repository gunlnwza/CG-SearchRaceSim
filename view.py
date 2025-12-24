import pygame as pg

from core import State, Point
from simulation import Simulation


class Game:
    X_MIN = 0
    X_MAX = 16000
    Y_MIN = 0
    Y_MAX = 9000
    WIDTH = X_MAX - X_MIN
    HEIGHT = Y_MAX - Y_MIN

    SCREEN_WIDTH = 800
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
        x = ((x - Game.X_MIN) * Game.SCREEN_WIDTH) // Game.WIDTH
        y = ((y - Game.Y_MIN) * Game.SCREEN_HEIGHT) // Game.HEIGHT
        return x, y

    def get_screen_length(self, length: int) -> float:
        res = (length * Game.SCREEN_WIDTH) // Game.WIDTH
        return res        

    def render_state(self, s: State):
        self.screen.fill("black")
        
        car = self.sim.state.car
        cp = self.sim.current_cp
        print(car, cp)

        pg.draw.circle(self.screen, "white", self.get_screen_point(cp), self.get_screen_length(cp.RADIUS))

        pg.draw.circle(self.screen, "red", self.get_screen_point(car), 5)

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
