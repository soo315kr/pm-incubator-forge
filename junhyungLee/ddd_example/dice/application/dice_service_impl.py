from dice.application.dice_service import DiceService
from dice.domain.dice import Dice

class DiceServiceImpl(DiceService):
    __instance: DiceService | None = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.dice_list: list[Dice] = [Dice()]

        return cls.__instance

    def add_dice(self) -> None:
        self.dice_list.append(Dice())

    def roll_all(self) -> list[int]:
        return [dice.roll() for dice in self.dice_list]
