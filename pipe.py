from constants import *


class Pipe:
    def __init__(self, x, y, position) -> None:
        self.img = PIPE_IMG
        self.x = x
        self.y = y
        self.position = position
        self.hitbox = self.img.get_rect()
        if position == TOP:
            self.img = pygame.transform.flip(
                self.img, flip_x=False, flip_y=True)
            self.hitbox.bottomleft = [x, y - round(PIPE_GAP / 2)]
        elif position == BOTTOM:
            self.hitbox.topleft = [x, y + round(PIPE_GAP / 2)]

    def draw(self, window) -> None:
        window.blit(self.img, self.hitbox)

    def update(self):
        self.hitbox.x -= SCROLL_SPEED
        self.x -= SCROLL_SPEED
