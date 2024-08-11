from node_gene import NodeGene
from connection_gene import ConnectionGene
from innovation_history import InnovationHistory, InnovationHistoryNode

import random


class Genome:
    def __init__(self) -> None:
        self.nodes: list[NodeGene] = []
        self.connections: list[ConnectionGene] = []

    def mutate(self, innovation_history) -> None:
        if self.connections == []:
            self.add_connection(innovation_history)

    def useful_connection(self, node1: int, node2: int) -> bool:
        same_layer = self.nodes[node1].layer == self.nodes[node2].layer
        already_exists = self.nodes[node1].is_connected_to(
            self.nodes[node2])

        return same_layer or already_exists

    def add_connection(self, innovation_history) -> None:
        node1 = random.randrange(0, self.nodes.length)
        node2 = random.randrange(0, self.nodes.length)

        while not self.useful_connection(node1, node2):
            node1 = random.randrange(0, self.nodes.length)
            node2 = random.randrange(0, self.nodes.length)

        if self.nodes[node1].layer > self.nodes[node2].layer:
            node1, node2 = node2, node1

        connection_innovation_number = self.get_innovation_number(
            innovation_history, self.nodes[node1], self.nodes[node2])

        self.connections.append(ConnectionGene(
            self.nodes[node1], self.nodes[node2], random.uniform(-1, 1), connection_innovation_number))

        # connect nodes

    def get_innovation_number(self, innovation_history: InnovationHistory, input: NodeGene, output: NodeGene):
        new = True
        current_innovation_number = innovation_history.next_innovation_number
        for i in range(len(innovation_history.data)):
            if innovation_history.data[i].matches(self, input, output):
                new = False
                current_innovation_number = innovation_history.data[i].innovation_number
                break

        if new:
            connected_innovation_numbers = []
            for i in range(len(self.connections)):
                connected_innovation_numbers.append(
                    self.connections[i].innovation_number)

            innovation_history.data.append(InnovationHistoryNode(
                input.id, output.id, current_innovation_number, connected_innovation_numbers))

            innovation_history.next_innovation_number += 1

        return current_innovation_number
