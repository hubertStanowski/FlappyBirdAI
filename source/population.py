from neat_config import NeatConfig
from innovation_history import InnovationHistory
from player import Player
from species import Species
from ground import Ground
from pipe import DoublePipeSet

import math
import pygame


class Population:
    def __init__(self, config: NeatConfig, size: int) -> None:
        self.config: NeatConfig = config
        self.size: int = size
        self.innovation_history: list[InnovationHistory] = []
        self.players: list[Player] = []
        self.species: list[Species] = []
        self.curr_best_player: Player = None
        self.prev_best_player: Player = None
        self.generation: int = 1
        self.staleness: int = 0

        for _ in range(size):
            self.players.append(Player())
            self.players[-1].genome.mutate(self.config,
                                           self.innovation_history)
            self.players[-1].genome.generate_network()

            # not necessary but nicely showcases largest network at the start
            if not self.curr_best_player or len(self.players[-1].genome.nodes) > len(self.curr_best_player.genome.nodes):
                self.curr_best_player = self.players[-1]

        self.prev_best_player = self.curr_best_player

    def update_survivors(self, window: pygame.Surface, ground: Ground, pipes: DoublePipeSet, node_id_renders: list) -> None:
        drawn_count = 0
        for player in self.players:
            if player.alive:
                player.look(ground, pipes)
                player.decide()

            if player.flying:
                player.update(ground, pipes)

            if ((player.flying and self.config.show_dying) or player.alive) and drawn_count < self.config.get_draw_limit():
                player.draw(window, sensor_view=self.config.sensor_view)
                drawn_count += 1

            # not necessary but if possible show a bigger network
            if player.score > self.curr_best_player.score or (player.score == self.curr_best_player.score and (len(player.genome.connections) > len(self.curr_best_player.genome.connections))):
                self.curr_best_player = player

        if self.config.sensor_view:
            self.curr_best_player.draw_network(window, node_id_renders)

    def natural_selection(self) -> None:
        # Happens after at least one generation so there will always be prev_best_player
        if self.prev_best_player.score >= self.curr_best_player.score:
            self.staleness += 1
        else:
            self.staleness = 0
        self.prev_best_player = self.curr_best_player

        self.speciate()
        self.update_fitness()
        self.sort()
        self.remove_low_performers_from_species()
        self.kill_low_performing_species()
        self.kill_stale_species()

        average_fitness_sum = self.get_avg_fitness_sum()
        self.players = []
        for s in self.species:
            self.players.append(s.representative.clone())
            children_count = math.floor((s.average_fitness /
                                         average_fitness_sum * len(self.players)) - 1)

            for _ in range(children_count):
                self.players.append(s.reproduce(
                    self.config, self.innovation_history))

        if len(self.players) < self.size:
            self.players.append(self.prev_best_player.clone())

        while len(self.players) < self.size:
            self.players.append(self.species[0].reproduce(
                self.config, self.innovation_history))

        self.generation += 1
        for player in self.players:
            if player:
                player.genome.generate_network()

    def finished(self) -> bool:
        for player in self.players:
            if player.alive or (player.flying and self.config.show_dying):
                return False
        return True

    def speciate(self) -> None:
        for s in self.species:
            s.players = []

        for player in self.players:
            assigned = False
            for s in self.species:
                if s.is_this_species(self.config, player.genome):
                    s.add(player)
                    assigned = True
                    break
            if not assigned:
                self.species.append(Species(player))

    def kill_low_performing_species(self) -> None:
        average_fitness_sum = self.get_avg_fitness_sum()
        kill_list = []

        for i in range(len(self.species)):
            if (self.species[i].average_fitness / average_fitness_sum * len(self.players)) < 1:
                kill_list.append(i)

        for i in kill_list:
            self.species.pop(i)

    def remove_low_performers_from_species(self) -> None:
        for species in self.species:
            species.remove_low_performers()
            species.share_fitness()
            species.update_average_fitness()

    def kill_stale_species(self) -> None:
        kill_list = []
        # starting at idx 2 so that top 2 species survive even if they are stale (used after sorting)
        for i in range(2, len(self.species)):
            if self.species[i].staleness >= self.config.get_species_staleness_limit():
                kill_list.append(i)

        for i in kill_list:
            self.species.pop(i)

    def sort(self) -> None:
        for s in self.species:
            s.sort()

        self.species.sort(key=lambda s: s.best_fitness, reverse=True)

    def update_fitness(self) -> None:
        for player in self.players:
            player.update_fitness()

    def get_avg_fitness_sum(self) -> float:
        return sum(species.average_fitness for species in self.species)
