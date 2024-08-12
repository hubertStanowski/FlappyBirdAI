class NeatConfig:
    def __init__(self) -> None:
        self.next_innovation_number: int = 1

    def get_next_innovation_number(self) -> int:
        return self.get_next_innovation_number

    def update_next_innovation_number(self) -> int:
        self.next_innovation_number += 1
