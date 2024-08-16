from constants import *

import pygame


class Ground:
    def __init__(self) -> None:
        self.img = GROUND_IMG
        self.hitbox = self.img.get_rect()
        self.hitbox.topleft = (0, WINDOW_HEIGHT-self.hitbox.height)

    def draw(self, window, sensor_view=False):
        window.blit(GROUND_IMG, self.hitbox)
        if sensor_view:
            pygame.draw.line(window, RED, (self.hitbox.left,
                             self.hitbox.top), (self.hitbox.right, self.hitbox.top), 4)

    def update(self):
        self.hitbox.x -= SCROLL_SPEED
        if abs(self.hitbox.x) > 50:
            self.hitbox.x = 0

    def collides(self, player):
        return self.hitbox.colliderect(player.hitbox)
