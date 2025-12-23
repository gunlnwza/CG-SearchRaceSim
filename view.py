import pygame as pg

pg.init()

WIDTH = 500
HEIGHT = 500
FPS = 30

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

def run():
    while True:
        dt = clock.tick(FPS)

        for e in pg.event.get():
            match e.type:
                case pg.QUIT:
                    return
                case pg.KEYDOWN:
                    match e.key:
                        case pg.K_q:
                            return

run()
pg.quit()
