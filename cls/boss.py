import random

from cls.enemy import Enemy


class Boss(Enemy):
    def __init__(self, first_enemy_choice):
        super().__init__("Calanthur", health=250, damage=50)
        self.base_type = first_enemy_choice
        self.shield = False
        self.thornmail = False
        self.lifesteal = False
        self.passive_description = ""

        if first_enemy_choice == "Mancubus":
            self.shield = True
            self.passive_description = "🛡️ The Dark Lord may shield himself from your attacks."
        elif first_enemy_choice == "Caragor":
            self.thornmail = True
            self.health += 40
            self.passive_description = "🪓 His sawtoothed armour reflects some damage back to you."
        elif first_enemy_choice == "Nazgul":
            self.lifesteal = True
            self.passive_description = "💉 The Dark Lord heals for 20% of the damage he deals."

    def boss_attack(self, player):
        damage_result = player.take_damage(self.damage)

        if isinstance(damage_result, tuple):
            damage_taken, passive_msg = damage_result
        else:
            damage_taken = damage_result
            passive_msg = ""

        lifesteal_message = ""
        if self.lifesteal:
            heal = int(damage_taken * 0.2)
            self.health += heal
            lifesteal_message = f"💉 {self.name} heals for {heal} HP!"

        message = f"{self.name} hits you for {damage_taken} damage."
        if passive_msg:
            message += f"\n{passive_msg}"

        return damage_taken, lifesteal_message

    def take_damage(self, amount):
        shield_triggered = False
        thornmail_triggered = False

        if self.shield and random.random() < 0.3:
            shield_triggered = True
            return 0, shield_triggered, thornmail_triggered

        damage_taken = super().take_damage(amount)

        if self.thornmail:
            thornmail_triggered = True

        return damage_taken, shield_triggered, thornmail_triggered
