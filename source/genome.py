from node_gene import NodeGene
from connection_gene import ConnectionGene
from innovation_history import InnovationHistory
from neat_config import NeatConfig

import random


class Genome:
    def __init__(self) -> None:
        self.nodes: list[NodeGene] = []
        self.connections: list[ConnectionGene] = []

    def mutate(self, innovation_history: list[InnovationHistory]) -> None:
        if self.connections == []:
            self.add_connection(innovation_history)

    def useful_connection(self, node1: int, node2: int) -> bool:
        same_layer = self.nodes[node1].layer == self.nodes[node2].layer
        already_exists = self.nodes[node1].is_connected_to(
            self.nodes[node2])

        return same_layer or already_exists

    def add_connection(self, config: NeatConfig, innovation_history: list[InnovationHistory]) -> None:
        # if all connected return

        node1 = random.randrange(0, self.nodes.length)
        node2 = random.randrange(0, self.nodes.length)

        while not self.useful_connection(node1, node2):
            node1 = random.randrange(0, self.nodes.length)
            node2 = random.randrange(0, self.nodes.length)

        if self.nodes[node1].layer > self.nodes[node2].layer:
            node1, node2 = node2, node1

        connection_innovation_number = self.get_innovation_number(
            config, innovation_history, self.nodes[node1], self.nodes[node2])

        self.connections.append(ConnectionGene(
            self.nodes[node1], self.nodes[node2], random.uniform(-1, 1), connection_innovation_number))

        # connect nodes

    def get_innovation_number(self, config: NeatConfig, innovation_history: list[InnovationHistory], input: NodeGene, output: NodeGene):
        new = True
        current_innovation_number = config.get_next_innovation_number()
        for i in range(len(innovation_history)):
            if innovation_history[i].matches(self, input, output):
                new = False
                current_innovation_number = innovation_history[i].innovation_number
                break

        if new:
            connected_innovation_numbers = []
            for i in range(len(self.connections)):
                connected_innovation_numbers.append(
                    self.connections[i].innovation_number)

            innovation_history.append(InnovationHistory(
                input.id, output.id, current_innovation_number, connected_innovation_numbers))

            config.update_next_innovation_number()

        return current_innovation_number
