import random

from cls.player import Player


class Warrior(Player):
    def __init__(self, name):
        super().__init__(name, health=175, damage=50)
        self.potions = 3
        self.passive = "Second Wind"
        self.revived = False

    def take_damage(self, amount):
        damage_taken = super().take_damage(amount)
        message = ""
        if self.health <= 0 and not self.revived:
            self.health = 50
            self.revived = True
            message = "⚔️ Warrior's Second Wind activated! You revive with 50 HP."
        return damage_taken, message


import random

class Mage(Player):
    def __init__(self, name):
        super().__init__(name, health=125, damage=75)
        self.potions = 2
        self.passive = "Arcane Burn"

    def attack_enemy(self, enemy):
        # Normal attack
        damage_result = enemy.take_damage(self.damage)
        damage = damage_result[0] if isinstance(damage_result, tuple) else damage_result
        message = f"You deal {damage} damage to {enemy.name}."

        # Arcane Burn triggers with 50% chance
        if enemy.is_alive() and random.random() < 0.5:
            burn_damage = 15
            burn_result = enemy.take_damage(burn_damage)
            burn_amount = burn_result[0] if isinstance(burn_result, tuple) else burn_result
            message += f"\n🔥 Arcane Burn triggers! Deals {burn_amount} bonus damage."

        return damage, message

class Rogue(Player):
    def __init__(self, name):
        super().__init__(name, health=150, damage=60)
        self.potions = 1
        self.passive = "Shadow Strike"

    def attack_enemy(self, enemy):
        crit_chance = 0.35

        if random.random() < crit_chance:
            damage_result = enemy.take_damage(self.damage * 2)
            # ✅ If boss returns tuple, take only first element
            damage = damage_result[0] if isinstance(damage_result, tuple) else damage_result
            message = f"💥 Critical hit! You deal {damage} damage to {enemy.name}."
        else:
            damage_result = enemy.take_damage(self.damage)
            damage = damage_result[0] if isinstance(damage_result, tuple) else damage_result
            message = f"You deal {damage} damage to {enemy.name}."

        return damage, message
