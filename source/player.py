from constants import *
from pipe import DoublePipeSet
from ground import Ground
from genome import Genome
from neat_config import NeatConfig

import pygame
from collections import defaultdict


class Player:
    def __init__(self) -> None:
        self.img: pygame.Surface = PLAYER_IMG
        self.hitbox: pygame.Rect = self.img.get_rect()
        self.hitbox.center = (PLAYER_X, PLAYER_Y)
        self.vel: int = 0
        self.alive: bool = True
        self.flying: bool = True
        self.score: int = 0
        # NEAT
        self.fitness: float = 0
        self.lifespan: int = 0
        self.genome_inputs: int = 4
        self.genome_outputs: int = 1
        self.genome: Genome = Genome(self.genome_inputs, self.genome_outputs)
        self.vision: list[float] = []
        self.sensor_view_data: list[float] = []

    def draw(self, window: pygame.Surface, sensor_view: bool = False) -> None:
        if not self.flying and self.alive:
            current_img = self.img
        elif self.vel < 10:
            current_img = pygame.transform.rotate(self.img, 30)
        else:
            angle = max(30 - (self.vel - 10) * 12, -90)
            current_img = pygame.transform.rotate(self.img, angle)

        window.blit(current_img, self.hitbox)

        if self.alive:
            if sensor_view and self.sensor_view_data:
                for point in self.sensor_view_data:
                    pygame.draw.line(window, RED, self.hitbox.center, point, 2)

    def update(self, ground: Ground, pipes: DoublePipeSet) -> None:
        if not self.flying:
            return

        self.vel = min(self.vel + GRAVITY, FLAP_SPEED*2)
        self.hitbox.y += self.vel
        self.check_collisions(ground, pipes)

        if self.alive:
            self.lifespan += 1
            self.score = pipes.score

    def flap(self) -> None:
        if self.alive:
            self.flying = True
            self.vel = -FLAP_SPEED

    def check_collisions(self, ground: Ground, pipes: DoublePipeSet) -> None:
        for pipeset in pipes.pipesets:
            if pipeset.collides(self):
                self.alive = False

        if ground.collides(self):
            self.alive = False
            self.flying = False


# NEAT

    def clone(self) -> 'Player':
        clone = Player()
        clone.genome = self.genome.clone()
        clone.fitness = self.fitness
        clone.genome.generate_network()

        return clone

    def crossover(self, config: NeatConfig, other_parent: 'Player') -> 'Player':
        child = Player()
        child.genome = self.genome.crossover(config, other_parent.genome)
        child.genome.generate_network()

        return child

    def update_fitness(self) -> None:
        self.fitness = 1 + self.score**2 + self.lifespan / 10

    def look(self, ground: Ground, pipes: DoublePipeSet) -> None:
        def remap(value: float, start1: float, stop1: float, start2: float, stop2: float) -> float:
            # Remaps a value in range(start1, stop1) proportionately to range(start2, stop2) and returns it
            return (value - start1) / (stop1 - start1) * (stop2 - start2) + start2

        self.vision = []
        closest_pipeset = pipes.get_closest_pipeset()
        height_cap = WINDOW_HEIGHT-ground.hitbox.height - self.hitbox.height

        self.vision.append(remap(self.vel, -FLAP_SPEED, 2*FLAP_SPEED, -1, 1))
        self.vision.append(remap(closest_pipeset.top.hitbox.x -
                           self.hitbox.x, 0, WINDOW_WIDTH-self.hitbox.x, 0, 1))
        self.vision.append(
            remap(closest_pipeset.bottom.hitbox.top - self.hitbox.y, 0, height_cap, 0, 1))
        self.vision.append(
            remap(self.hitbox.y - closest_pipeset.top.hitbox.bottom, 0, height_cap, 0, 1))

        # For drawing when sensor_view is on
        self.sensor_view_data = []
        self.sensor_view_data.append(closest_pipeset.bottom.hitbox.topleft)
        self.sensor_view_data.append(closest_pipeset.top.hitbox.bottomleft)

    def decide(self) -> None:
        if not self.vision:
            return

        decision = self.genome.feed_forward(self.vision)[0]
        if decision > 0.6:
            self.flap()

# Here and not in genome.py as that file is meant to be reusable and this function is not
    def draw_network(self, window: pygame.Surface, node_id_renders: list[pygame.Surface]) -> None:
        if not self.genome.network:
            return

        radius = 12
        x = WINDOW_WIDTH - radius*1.5
        y = WINDOW_HEIGHT - radius*1.5
        layer_count = self.genome.layer_count - 1
        y_diff = radius * 3
        x_diff = radius * 5

        layers = defaultdict(list)
        for node in self.genome.network:
            layers[node.layer].append(node)

        node_pos = {}

        for layer, nodes in layers.items():
            # Hardcoding as there have never been >5 nodes in a layer and don't want to overcomplicate it for nodes to look good
            y_positions = [y - 2*y_diff, y -
                           y_diff, y - 3*y_diff, y, y-4*y_diff]
            for i, node in enumerate(nodes):
                node_pos[node] = (x-(layer_count-layer)*x_diff, y_positions[i])

        for connection in self.genome.connections:
            input_pos = node_pos[connection.input]
            output_pos = node_pos[connection.output]
            pygame.draw.line(window, BLUE, input_pos,
                             output_pos, max(int(5 * abs(connection.weight)), 1))

        # Seperate loop and not when assigning positions so that the connection line doesn't overlay the id
        for node, pos in node_pos.items():
            text = node_id_renders[node.id]
            text_rect = text.get_rect(center=node_pos[node])

            pygame.draw.circle(window, BLACK, node_pos[node], radius+2)
            pygame.draw.circle(window, RED, node_pos[node], radius)
            window.blit(text, text_rect)
