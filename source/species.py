from player import Player


class Species:
    def __init__(self, representative: Player) -> None:
        self.players: list[Player] = [representative]
        # TODO clone instead of direct pointer fo self.representative
        self.representative: Player = representative
        self.max_fitness: float = self.representative.fitness
        self.average_fitness: float = self.max_fitness
        # if max_fitness of the species doesn't improve in 15 generations (number given by creators of NEAT) -> don't allow reproduction
        self.staleness: int = 0

    def add(self, new: Player) -> None:
        self.players.append(new)

    def update_average_fitness(self) -> None:
        self.average_fitness = sum(
            [player.fitness for player in self.players]) / len(self.players)

    def sort(self) -> None:
        if len(self.players) == 0:
            self.staleness = 100
            return

        # Sort self.players in descending order by fitness
        self.players.sort(key=lambda player: player.fitness, reverse=True)

        if self.players[0].fitness > self.max_fitness:
            self.staleness = 0
            self.max_fitness = self.players[0].fitness
            # TODO clone instead of direct pointer fo self.representative
            self.representative = self.players[0]
        else:
            self.staleness += 1

    def share_fitness(self) -> None:
        for player in self.players:
            player.fitness /= len(self.players)

    def remove_low_performers(self) -> None:
        """
            Removes the bottom half of the players.
            !ONLY USE AFTER SORTING!
        """
        if len(self.players) <= 2:
            return

        for _ in range(len(self.players) // 2):
            self.players.pop()

    def get_average_weight_difference(self, genome1, genom2) -> float:
        return 0.0

    def get_excess_and_disjoint_count(self, genome1, genome2) -> int:
        return 0
