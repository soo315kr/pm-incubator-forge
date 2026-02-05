# domain/dice.py
import random

class Dice:
    """도메인 객체: 주사위"""
    SIDES = 6  # 고정 6면

    def roll(self) -> int:
        """주사위를 굴려 1 ~ 6 사이 결과 반환"""
        return random.randint(1, self.SIDES)
