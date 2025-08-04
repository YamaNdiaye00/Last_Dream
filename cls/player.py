from cls.character import Character


class Player(Character):
    def __init__(self, name: str, health: int, damage: int):
        super().__init__(name, health, damage)
        self.potions = 0

    def use_potion(self):
        if self.potions > 0:
            heal_amount = 50
            self.health += heal_amount
            self.potions -= 1
            print(f"You used a potion and healed {heal_amount} HP. Remaining potions: {self.potions}")
        else:
            print("No potions left!")
