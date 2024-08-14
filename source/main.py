from constants import *
from player import Player
from ground import Ground
from pipe import DoublePipeSet
from population import Population

import pygame


def main():
    pygame.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption("Flappy Bird AI")

    clock = pygame.time.Clock()
    ground = Ground()
    pipes = DoublePipeSet()
    h_player = Player()
    h_player.flying = False
    population = Population(size=100)

    human_playing = False

    while True:
        clock.tick(60)

        window.blit(BACKGROUND_IMG, (0, 0))
        pipes.update()
        pipes.draw(window)
        if h_player.alive:
            ground.update()
        ground.draw(window)

        if human_playing:
            h_player.draw(window)
            h_player.update(ground)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        h_player.flying = True
                        h_player.flap()
        else:
            if not population.finished():
                population.update_survivors(window, ground, pipes)
            else:
                population.natural_selection()
                pipes = DoublePipeSet()
                print(population.generation)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

        pygame.display.update()


if __name__ == "__main__":
    main()
