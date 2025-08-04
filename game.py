import random

from cls.boss import Boss
from cls.enemy import Enemy
from narrative import Narrative
from cls.player_classes import Warrior, Mage, Rogue


class Game:
    def __init__(self):
        self.player = None
        self.first_enemy_choice = None

    def start(self):
        print(Narrative.intro())
        name = input("\nEnter your character's name: ")
        self.choose_class(name)
        self.first_encounter()
        if self.player.is_alive():
            self.boss_encounter()
        print("Game Over!")

    def battle(self, enemy: Enemy):
        """Handles normal enemy battles."""
        print(f"A wild {enemy.name} appears!")
        while self.player.is_alive() and enemy.is_alive():
            self.display_status(enemy)
            action = input("Choose action: [attack/potion/run]: ").lower()
            if action == "attack":
                if hasattr(self.player, "attack_enemy"):
                    self.player.attack_enemy(enemy)
                else:
                    damage = enemy.take_damage(self.player.damage)
                    print(f"You deal {damage} damage to {enemy.name}.")
                if enemy.is_alive():
                    damage = enemy.damage
                    self.player.take_damage(damage)
                    print(f"{enemy.name} hits you for {damage} damage.")

            elif action == "potion":
                self.player.use_potion()
            elif action == "run":
                print("You ran away!")
                return False

        return self.player.is_alive()

    def first_encounter(self):
        """Randomly selects one of three enemies."""
        enemy_names = ["Mancubus", "Caragor", "Nazgul"]
        self.first_enemy_choice = random.choice(enemy_names)
        enemy = Enemy(self.first_enemy_choice, health=75, damage=25)

        print("\n--- First Encounter ---")
        survived = self.battle(enemy)
        if survived:
            print(f"You defeated {self.first_enemy_choice}!")
        else:
            print("You were defeated in the first encounter.")

    def boss_encounter(self):
        """Handles the final boss battle."""
        print("\n--- Boss Encounter ---")
        boss = Boss(self.first_enemy_choice)
        survived = self.battle_boss(boss)

        if survived:
            print(f"You have defeated the {boss.name} and won the game!")
        else:
            print(f"The {boss.name} has defeated you...")

    def battle_boss(self, boss: Boss):
        """Boss battle loop with passives."""
        print(f"A wild {boss.name} appears!")
        while self.player.is_alive() and boss.is_alive():
            self.display_status(boss)
            action = input("Choose action: [attack/potion/run]: ").lower()
            if action == "attack":
                damage, thornmail_trigger = boss.take_damage(self.player.damage)
                if damage > 0:
                    print(f"You deal {damage} damage to {boss.name}.")
                if thornmail_trigger:
                    thorns = 5
                    self.player.take_damage(thorns)
                    print(f"🩸 Thornmail damages you for {thorns} HP!")
                if boss.is_alive():
                    boss.boss_attack(self.player)

            elif action == "potion":
                self.player.use_potion()
            elif action == "run":
                print("You ran away!")
                return False

        return self.player.is_alive()

    def choose_class(self, name):
        """Class selection with validation, stats display, passive explanation."""
        while True:
            print(Narrative.class_select())
            print("1. Warrior")
            print("2. Mage")
            print("3. Rogue\n")

            choice = input("> ")

            # Validate choice
            if choice not in ["1", "2", "3"]:
                print(
                    "\nYou are supposed to be the One to save us all!\n"
                    "Act like it and heed my words.\n"
                    "Choose between the 3 boons I've presented you!\n"
                )
                continue

            # Assign chosen class
            if choice == "1":
                self.player = Warrior(name)
                print("\nThe Warrior: Trample your enemies with your might")
                passive = self.player.passive
            elif choice == "2":
                self.player = Mage(name)
                print("\nThe Mage: Smite your enemies with your Fire magic")
                passive = self.player.passive
            else:
                self.player = Rogue(name)
                print("\nThe Rogue: Swift as the wind")
                passive = self.player.passive

            # Display stats
            print("\n--- Your Chosen Class Stats ---")
            print(f"Health Points = {self.player.health}")
            print(f"Damage = {self.player.damage}")
            print(f"Potions = {self.player.potions}")
            print(f"Passive: {passive}")
            print("--------------------------------\n")

            # Confirm choice
            confirm = input("Do you choose this class? (Yes to Confirm): ").lower()
            if confirm == "yes":
                break
            else:
                print("\nThen choose another:\n")

    def display_status(self, enemy):
        """Display enemy and player HP with potion count."""
        print(f"\n{enemy.name} HP: {enemy.health}")
        print(f"{self.player.name} HP: {self.player.health} | Potions: {self.player.potions}\n")

    def create_first_enemy(self):
        """Creates the first random enemy for GUI mode."""
        import random
        from cls.enemy import Enemy

        enemy_names = ["Mancubus", "Caragor", "Nazgul"]
        self.first_enemy_choice = random.choice(enemy_names)
        return Enemy(self.first_enemy_choice, health=100, damage=25)

    def create_boss(self, first_enemy_name=None):
        """Creates the boss for GUI mode based on first encounter."""
        from cls.boss import Boss
        # If GUI didn't set first_enemy_choice yet
        if first_enemy_name:
            self.first_enemy_choice = first_enemy_name
        return Boss(self.first_enemy_choice)


if __name__ == "__main__":
    game = Game()
    game.start()
