from player import Player


class Species:
    def __init__(self, representative: Player) -> None:
        self.players: list[Player] = [representative]
        # TODO clone instead of direct pointer of the self.representative
        self.representative: Player = representative
        self.max_fitness: float = self.representative.fitness
        self.average_fitness: float = self.max_fitness
        # if max_fitness of the species doesn't improve in 15 generations, don't allow reproduction
        self.staleness: int = 0

    def add(self, new: Player) -> None:
        self.players.append(new)

    def update_average_fitness(self) -> None:
        self.average_fitness = sum(
            [player.fitness for player in self.players]) / len(self.players)
