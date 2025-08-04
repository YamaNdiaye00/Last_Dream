from cls.character import Character


class Enemy(Character):
    def __init__(self, name: str, health: int, damage: int):
        super().__init__(name, health, damage)
