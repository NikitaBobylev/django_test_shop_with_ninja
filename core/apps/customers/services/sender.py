from abc import (
    ABC,
    abstractmethod,
)


class BaseSendersService(ABC):
    @abstractmethod
    def send_code(self, code: str) -> None:
        ...
