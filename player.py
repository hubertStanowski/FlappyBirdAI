from constants import *
from pipe import PipeSet

from collections import deque


class Player:
    def __init__(self, x, y) -> None:
        self.img = PLAYER_IMG
        self.hitbox = self.img.get_rect()
        self.hitbox.center = (x, y)
        self.vel_y = 0
        self.pipes = deque([PipeSet(), PipeSet(x_offset=WINDOW_WIDTH//2)])
        self.alive = True
        self.on_ground = False

    def draw(self, window) -> None:
        for pipeset in self.pipes:
            pipeset.draw(window)

        window.blit(self.img, self.hitbox)

    def update(self):
        self.vel_y += GRAVITY
        self.hitbox.y += self.vel_y

        self.check_collisions()

        change = False
        for pipeset in self.pipes:
            pipeset.update()
            if pipeset.is_offscreen():
                change = True

        if change:
            self.pipes.popleft()
            self.pipes.append(PipeSet())

    def flap(self):
        if self.alive:
            self.vel_y = -8

    def check_collisions(self):
        for pipeset in self.pipes:
            if pipeset.collides(self):
                self.alive = False
                return True

        return False
