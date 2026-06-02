from dataclasses import dataclass


@dataclass
class Player:
    id: int
    name: str
    gyullas_pool: int = 0
    gyullas_vault: int = 0

    @property
    def total_gyullas(self) -> int:
        return self.gyullas_pool + self.gyullas_vault
