from constants import *
from player import Player
from ground import Ground
from pipe import DoublePipeSet
from population import Population
from neat_config import NeatConfig

import pygame


def main():
    pygame.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption("Flappy Bird NEAT AI")

    clock = pygame.time.Clock()
    ground = Ground()
    pipes = DoublePipeSet()
    h_player = Player()
    h_player.flying = False

    """
        With small population it is possible that NEAT will have to be redone ("RESET" message), but with big population
        it is likely that there will be no need for evolution due to how uncomplicated FlappyBird is
    """
    config = NeatConfig()
    population = Population(config, size=50)

    human_playing = True
    show_fps = True
    fps = 60

    # temp = True
    # while temp:
    #     for event in pygame.event.get():
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_SPACE:
    #                 temp = False

    while True:
        clock.tick(fps)

        window.blit(BACKGROUND_IMG, (0, 0))

        if h_player.flying or not human_playing:
            pipes.update(h_player.hitbox.x)
        pipes.draw(window)

        if h_player.alive or not human_playing:
            ground.update()
        ground.draw(window)

        if human_playing:
            h_player.draw(window)
            h_player.update(ground, pipes)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        h_player.flap()

            score = h_player.score
        else:
            if not population.finished():
                population.update_survivors(window, ground, pipes)
            else:
                population.natural_selection()
                pipes = DoublePipeSet()
            # print(([player.score for player in population.players if player.alive]))

            if population.staleness >= 5:
                population = Population(config, population.size)
                pipes = DoublePipeSet()
                display_reset(window)

            score = population.gen_best_score
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    # Plus is on the same key as equals on most keyboards so checking for equals
                    if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                        fps = min(240, fps+10)
                    elif event.key == pygame.K_MINUS:
                        fps -= 10
                        if fps < 10:
                            fps = 10
                    elif event.key == pygame.K_d:
                        config.toggle_show_dying()

            display_generation(window, population)
            if show_fps:
                display_fps(window, fps)

        display_score(window, score)

        pygame.display.update()


def display_generation(window, population: Population):
    current_generation = population.generation
    font = pygame.font.SysFont(FONT, GENERATION_FONT_SIZE)
    label = font.render(f"Gen: {current_generation}", True, BLACK)
    label_rect = label.get_rect(topleft=(10, 10))

    window.blit(label, label_rect)


def display_score(window, score):
    font = pygame.font.SysFont(FONT, SCORE_FONT_SIZE)
    label = font.render(str(score), True, BLACK)
    label_rect = label.get_rect(center=(WINDOW_WIDTH // 2, 30))

    window.blit(label, label_rect)


def display_reset(window):
    font = pygame.font.SysFont(FONT, RESET_FONT_SIZE)
    label = font.render("RESET", True, RED)
    label_rect = label.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 5))

    window.blit(label, label_rect)
    pygame.display.update()
    pygame.time.delay(1000)


def display_fps(window, fps):
    font = pygame.font.SysFont(FONT, FPS_FONT_SIZE)
    label = font.render(f"FPS: {fps}", True, BLACK)
    label_rect = label.get_rect(bottomleft=(10, WINDOW_HEIGHT-10))

    window.blit(label, label_rect)


if __name__ == "__main__":
    main()
