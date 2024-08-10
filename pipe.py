from constants import *
import random


class Pipe:
    def __init__(self, x, y, position) -> None:
        self.img = PIPE_IMG
        self.hitbox = self.img.get_rect()
        if position == TOP:
            self.img = pygame.transform.flip(
                self.img, flip_x=False, flip_y=True)
            self.hitbox.bottomleft = (x, y - round(PIPE_GAP / 2))
        else:
            self.hitbox.topleft = (x, y + round(PIPE_GAP / 2))

    def draw(self, window) -> None:
        window.blit(self.img, self.hitbox)

    def update(self):
        self.hitbox.x -= SCROLL_SPEED


class PipeSet:
    def __init__(self, x_offset=0) -> None:
        pipe_height = random.randint(-100, 100)
        self.bottom = Pipe(WINDOW_WIDTH+x_offset,
                           WINDOW_HEIGHT // 2 + pipe_height, BOTTOM)
        self.top = Pipe(WINDOW_WIDTH+x_offset,
                        WINDOW_HEIGHT // 2 + pipe_height, TOP)

    def draw(self, window):
        self.bottom.draw(window)
        self.top.draw(window)

    def update(self):
        self.bottom.update()
        self.top.update()

    def is_offscreen(self):
        return self.bottom.hitbox.right < 0

    def collides(self, player):
        return self.bottom.hitbox.colliderect(player.hitbox) or self.top.hitbox.colliderect(player.hitbox)
