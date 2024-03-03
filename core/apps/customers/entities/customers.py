from dataclasses import dataclass


@dataclass
class Customer:
    id: int
    phone: str

    def __str__(self):
        return self.phone
