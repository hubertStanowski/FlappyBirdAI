from constants import *

import random
from collections import deque


class Pipe:
    def __init__(self, x, y, position) -> None:
        self.img = PIPE_IMG
        self.hitbox = self.img.get_rect()
        if position == TOP:
            self.img = pygame.transform.flip(
                self.img, flip_x=False, flip_y=True)
            self.hitbox.bottomleft = (x, y - (PIPE_GAP // 2))
        else:
            self.hitbox.topleft = (x, y + (PIPE_GAP // 2))

    def draw(self, window) -> None:
        window.blit(self.img, self.hitbox)

    def update(self):
        self.hitbox.x -= SCROLL_SPEED


class PipeSet:
    def __init__(self, x_offset=0) -> None:
        pipe_height = random.randint(-200, 150)
        self.bottom = Pipe(WINDOW_WIDTH+x_offset,
                           WINDOW_HEIGHT // 2 + pipe_height, BOTTOM)
        self.top = Pipe(WINDOW_WIDTH+x_offset,
                        WINDOW_HEIGHT // 2 + pipe_height, TOP)
        self.passed = False

    def draw(self, window):
        self.bottom.draw(window)
        self.top.draw(window)

    def update(self):
        self.bottom.update()
        self.top.update()

    def is_offscreen(self):
        return self.bottom.hitbox.right < 0

    def collides(self, player):
        on_screen = self.bottom.hitbox.colliderect(
            player.hitbox) or self.top.hitbox.colliderect(player.hitbox)

        off_screen = (self.top.hitbox.x ==
                      player.hitbox.x) and player.hitbox.y < 0

        return on_screen or off_screen

    def check_passed(self, player_hitbox_x):
        if self.top.hitbox.right < player_hitbox_x and not self.passed:
            self.passed = True
            return True

        return False


class DoublePipeSet:
    def __init__(self) -> None:
        self.pipesets: deque[PipeSet] = deque(
            [PipeSet(), PipeSet(x_offset=PIPE_SEPERATION)])
        self.score = 0

    def draw(self, window) -> None:
        for pipeset in self.pipesets:
            pipeset.draw(window)

    def update(self, player_hitbox_x) -> None:
        change = False
        for pipeset in self.pipesets:
            pipeset.update()
            if pipeset.is_offscreen():
                change = True
            if pipeset.check_passed(player_hitbox_x):
                self.score += 1

        if change:
            self.pipesets.popleft()
            self.pipesets.append(PipeSet())
