from constants import *
from pipe import PipeSet


class Player:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.img = PLAYER_IMG
        self.vel_y = 0
        self.pipes = [PipeSet(), PipeSet(x_offset=WINDOW_WIDTH//2)]

    def draw(self, window) -> None:
        for pipeset in self.pipes:
            pipeset.draw(window)

        window.blit(self.img, (self.x, self.y))

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

        for pipeset in self.pipes:
            pipeset.update()

    def flap(self):
        self.vel_y = -10
