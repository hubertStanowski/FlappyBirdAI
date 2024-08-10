from constants import *
from pipe import PipeSet
from ground import Ground

from collections import deque


class Player:
    def __init__(self, x, y) -> None:
        self.img = PLAYER_IMG
        self.hitbox = self.img.get_rect()
        self.hitbox.center = (x, y)
        self.vel_y = 0
        self.pipes = deque([PipeSet(), PipeSet(x_offset=PIPE_SEPERATION)])
        self.ground = Ground()
        self.alive = True
        self.on_ground = False

    def draw(self, window) -> None:
        for pipeset in self.pipes:
            pipeset.draw(window)

        self.ground.draw(window)
        window.blit(self.img, self.hitbox)

    def update(self):
        if self.on_ground:
            return

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

        self.ground.update()

    def flap(self):
        if self.alive:
            self.vel_y = -FLAP_SPEED

    def check_collisions(self):
        for pipeset in self.pipes:
            if pipeset.collides(self):
                self.alive = False

        self.on_ground = self.ground.collides(self)
        if self.on_ground:
            self.alive = False

        return self.alive
