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
    # lower this if lagging
    config.draw_limit = 200
    # if you are impatient lower this, but recommended above 5
    config.population_staleness_limt = 10

    node_id_renders = prerender_node_ids()
    population = Population(config, size=75)

    human_playing = False
    show_fps = True

    # With big population or sensor_view enabled actual fps count will be lower optimally keep between 60-120
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

        if human_playing:
            ground.draw(window)
        else:
            ground.draw(window, sensor_view=config.sensor_view)

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
                population.update_survivors(
                    window, ground, pipes, node_id_renders)
            else:
                population.natural_selection()
                pipes = DoublePipeSet()

            if population.staleness >= config.get_population_staleness_limt() or (population.best_score == 0 and population.staleness >= config.get_population_staleness_limt() / 2):
                population = Population(config, population.size)
                pipes = DoublePipeSet()
                display_reset(window, ground)

            score = population.gen_best_score
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    # Plus is on the same key as equals on most keyboards so checking for equals
                    if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                        fps = min(FPS_HIGHER_BOUND, fps+10)
                    elif event.key == pygame.K_MINUS:
                        fps -= 10
                        if fps < FPS_LOWER_BOUND:
                            fps = FPS_LOWER_BOUND
                    elif event.key == pygame.K_d:
                        config.toggle_show_dying()
                    elif event.key == pygame.K_s:
                        config.toggle_sensor_view()
                        if config.sensor_view:
                            pygame.display.set_caption(
                                "Flappy Bird NEAT AI - SENSOR VIEW")
                        else:
                            pygame.display.set_caption("Flappy Bird NEAT AI")
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        population.staleness = config.population_staleness_limt

            display_generation(window, population)
            if config.sensor_view:
                display_alive_count(window, population)
            if show_fps or config.sensor_view:
                display_fps(window, fps, clock, advanced=config.sensor_view)

        display_score(window, score)

        pygame.display.update()


def display_generation(window, population: Population) -> None:
    current_generation = population.generation
    font = pygame.font.SysFont(FONT, GENERATION_FONT_SIZE)
    label = font.render(f"Gen: {current_generation}", True, BLACK)
    label_rect = label.get_rect(topleft=(10, 10))

    window.blit(label, label_rect)


def display_score(window, score: int) -> None:
    font = pygame.font.SysFont(FONT, SCORE_FONT_SIZE)
    label = font.render(str(score), True, BLACK)
    label_rect = label.get_rect(center=(WINDOW_WIDTH // 2, 30))

    window.blit(label, label_rect)


def display_reset(window, ground: Ground) -> None:
    font = pygame.font.SysFont(FONT, RESET_FONT_SIZE)
    label = font.render("RESET", True, RED)
    label_rect = label.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))

    window.blit(BACKGROUND_IMG, (0, 0))
    ground.draw(window)
    window.blit(label, label_rect)
    pygame.display.update()
    pygame.time.delay(1000)


def display_fps(window,  fps: int, clock, advanced: bool = False) -> None:
    font = pygame.font.SysFont(FONT, FPS_FONT_SIZE)
    actual = round(clock.get_fps(), 1)
    if advanced:
        label = font.render(f"FPS: {actual} ({fps})", True, RED)
    else:
        label = font.render(f"FPS: {fps}", True, BLACK)
    label_rect = label.get_rect(bottomleft=(10, WINDOW_HEIGHT-10))

    window.blit(label, label_rect)


def display_alive_count(window, population: Population) -> None:
    alive_count = len(
        [player for player in population.players if player.alive])

    font = pygame.font.SysFont(FONT, ALIVE_FONT_SIZE)
    label = font.render(f"Alive: {alive_count} / {population.size}", True, RED)
    label_rect = label.get_rect(topleft=(10, 50))

    window.blit(label, label_rect)


# Optimization for drawing neural network
def prerender_node_ids() -> list:
    renders = []
    font = pygame.font.Font(FONT, NODE_ID_FONT_SIZE)
    for id in range(8):
        renders.append(font.render(str(id), True, WHITE))

    return renders


if __name__ == "__main__":
    main()
