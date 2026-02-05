from abc import ABC, abstractmethod

class DiceService(ABC):
    """애플리케이션 서비스 인터페이스"""

    @abstractmethod
    def add_dice(self) -> None:
        pass

    @abstractmethod
    def roll_all(self) -> list[int]:
        pass
