from node_gene import NodeGene
from connection_gene import ConnectionGene


class Genome:
    def __init__(self) -> None:
        self.node_genes: list[NodeGene] = []
        self.connection_genes: list[ConnectionGene] = []

    def mutate(self) -> None:
        pass

    # def useful_connection(self, node1: int, node2: int) -> bool:
    #     same_layer = self.node_genes[node1].layer == self.node_genes[node2].layer
    #     already_exists = self.node_genes[node1].is_connected_to(
    #         self.node_genes[node2])

    #     return same_layer or already_exists

    def add_connection(self):
        pass
