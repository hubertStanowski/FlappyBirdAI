from constants import *
from player import Player
from pipe import Pipe

import pygame
import random


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption("Flappy Bird AI")

    clock = pygame.time.Clock()
    player = Player(WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2)
    ground_scroll = 0
    flying = False
    last_pipe = 0
    pipes = set()

    while True:
        clock.tick(60)
        window.blit(GROUND_IMG, (ground_scroll,
                    WINDOW_HEIGHT-GROUND_IMG.get_height()))
        window.blit(BACKGROUND_IMG, (0, 0))
        for pipe in pipes:
            pipe.draw(window)
            pipe.update()
        player.draw(window)

        ground_scroll -= SCROLL_SPEED

        if abs(ground_scroll) > 50:
            ground_scroll = 0

        pygame.display.update()
        if flying:
            player.move()
            current_time = pygame.time.get_ticks()
            if current_time - last_pipe > PIPE_FREQUENCY:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(WINDOW_WIDTH, int(
                    WINDOW_HEIGHT / 2) + pipe_height, BOTTOM)
                top_pipe = Pipe(WINDOW_WIDTH, int(
                    WINDOW_HEIGHT / 2) + pipe_height, TOP)
                pipes.add(btm_pipe)
                pipes.add(top_pipe)
                last_pipe = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flying = True
                    player.flap()


if __name__ == "__main__":
    main()
