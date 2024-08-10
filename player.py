from constants import *


class Player:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.img = PLAYER_IMG
        self.vel_x = HORIZONTAL_SPEED
        self.vel_y = 0

    def draw(self, window) -> None:
        window.blit(self.img, (self.x, self.y))

    def move(self):
        self.vel_y += GRAVITY

        self.x += self.vel_x

        if self.vel_y < 0:
            self.vel_y = max(self.vel_y, VERTICAL_SPEED_CAP)

        self.y += self.vel_y

    def flap(self):
        self.vel_y -= 20
