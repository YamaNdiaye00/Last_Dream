class Character:
    def __init__(self, name: str, health: int, damage: int):
        self.name = name
        self.health = health
        self.damage = damage

    def take_damage(self, amount: int):
        self.health = max(0, self.health - amount)
        return amount

    def is_alive(self):
        return self.health > 0
