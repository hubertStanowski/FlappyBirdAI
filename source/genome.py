from node_gene import NodeGene
from connection_gene import ConnectionGene
from innovation_history import InnovationHistory
from neat_config import NeatConfig

import random


class Genome:
    def __init__(self, inputs: int, outputs: int, crossover: bool = False) -> None:
        self.nodes: list[NodeGene] = []
        self.connections: list[ConnectionGene] = []
        # each genome consists of at least 1 input and 1 output layer (can have more hidden ones later on)
        self.inputs: int = inputs
        self.outputs: int = outputs
        self.layer_count: int = 2
        self.next_node_id: int = 0

        if crossover:
            return

        for _ in range(self.inputs):
            self.nodes.append(NodeGene(self.next_node_id))
            self.nodes[self.next_node_id].layer = 0
            self.next_node_id += 1

        for _ in range(self.outputs):
            self.nodes.append(NodeGene(self.next_node_id))
            self.nodes[self.next_node_id].layer = 1
            self.next_node_id += 1

        self.bias_node = NodeGene(self.next_node_id)
        self.bias_node.layer = 0
        self.nodes.append(self.bias_node)
        self.next_node_id += 1

    def mutate(self, innovation_history: list[InnovationHistory]) -> None:
        if self.connections == []:
            self.add_connection(innovation_history)

    def useful_connection(self, node1: int, node2: int) -> bool:
        same_layer = self.nodes[node1].layer == self.nodes[node2].layer
        already_exists = self.nodes[node1].is_connected_to(
            self.nodes[node2])

        return same_layer or already_exists

    def add_connection(self, config: NeatConfig, innovation_history: list[InnovationHistory]) -> None:
        if self.fully_connected():
            return

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

        self.connect_nodes()

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

    def fully_connected(self):
        possible_connections = 0
        nodes_per_layer = [0 for _ in range(self.layer_count)]

        for i in range(len(self.nodes)):
            nodes_per_layer[self.nodes[i].layer] += 1

        # possible connections for each layer are (node count of this layer) * (node count of all layers in front of it)
        for i in range(self.layer_count - 1):
            nodes_in_front = 0
            for j in range(i+1, self.layer_count):
                nodes_in_front += nodes_per_layer[j]

            possible_connections *= nodes_per_layer[i] * nodes_in_front

        return possible_connections <= len(self.connections)

    def connect_nodes(self):
        for i in range(len(self.nodes)):
            self.nodes[i].output_connections = []

        for i in range(len(self.connections)):
            self.connections[i].input.output_connections.append(
                self.connections[i])
