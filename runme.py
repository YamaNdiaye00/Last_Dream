import os
import sys
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

from cls.player_classes import Warrior, Mage, Rogue
from game import Game
from narrative import Narrative


def resource_path(relative_path):
    """ Get absolute path to resource for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS  # Temporary folder for PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class RPGGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Last Dream")
        self.root.geometry("800x600")
        self.game = Game()
        self.player_name = tk.StringVar()
        self.current_enemy = None
        self.is_boss_fight = False
        self.intro_screen()

    # ---------- INTRO SCREEN ----------
    def intro_screen(self):
        self.clear_screen()
        tk.Label(self.root, text=Narrative.intro(),
                 font=("Times New Roman", 16), wraplength=700, justify="left").pack(pady=20)
        tk.Button(self.root, text="Continue", font=("Arial", 14),
                  command=self.start_screen).pack(pady=20)

    # ---------- START SCREEN ----------
    def start_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome to the Python RPG",
                 font=("Times New Roman", 24)).pack(pady=20)

        tk.Label(self.root, text="Enter your character's name:",
                 font=("Arial", 14)).pack()
        tk.Entry(self.root, textvariable=self.player_name,
                 font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text=Narrative.class_select(),
                 font=("Arial", 14), wraplength=700, justify="left").pack(pady=20)

        tk.Label(self.root, text="Choose your class:",
                 font=("Arial", 16)).pack(pady=10)

        # Load images
        warrior_img = Image.open(resource_path("assets/enemies/player/warrior.png")).resize((150, 150))
        mage_img = Image.open(resource_path("assets/enemies/player/mage.png")).resize((150, 150))
        rogue_img = Image.open(resource_path("assets/enemies/player/rogue.png")).resize((150, 150))

        self.warrior_photo = ImageTk.PhotoImage(warrior_img)
        self.mage_photo = ImageTk.PhotoImage(mage_img)
        self.rogue_photo = ImageTk.PhotoImage(rogue_img)

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        def on_enter(btn): btn.config(bg="lightblue")

        def on_leave(btn): btn.config(bg="SystemButtonFace")

        for idx, (name, img, cls) in enumerate([
            ("Warrior", self.warrior_photo, "1"),
            ("Mage", self.mage_photo, "2"),
            ("Rogue", self.rogue_photo, "3")
        ]):
            col_frame = tk.Frame(frame)
            col_frame.grid(row=0, column=idx, padx=20)
            tk.Label(col_frame, image=img).pack()
            btn = tk.Button(col_frame, text=name, font=("Arial", 14),
                            command=lambda c=cls: self.select_class(c))
            btn.pack()
            btn.bind("<Enter>", lambda e, b=btn: on_enter(b))
            btn.bind("<Leave>", lambda e, b=btn: on_leave(b))

    def select_class(self, choice):
        name = self.player_name.get()
        if not name:
            messagebox.showwarning("Missing Name", "Please enter your name first.")
            return

        self.game.player = {
            "1": Warrior,
            "2": Mage,
            "3": Rogue
        }[choice](name)

        messagebox.showinfo(
            "Class Selected",
            f"You chose {self.game.player.__class__.__name__}!\n"
            f"HP: {self.game.player.health}, Damage: {self.game.player.damage}, "
            f"Potions: {self.game.player.potions}\n"
            f"Passive: {self.game.player.passive}"
        )
        self.first_encounter_intro()

    # ---------- FIRST ENCOUNTER ----------
    def first_encounter_intro(self):
        """Intro screen for the first encounter."""
        self.clear_screen()
        self.current_enemy = self.game.create_first_enemy()

        # ✅ Store the type of the first enemy for boss mapping
        self.game.first_enemy_choice = self.current_enemy.name
        self.is_boss_fight = False

        tk.Label(self.root, text=Narrative.first_encounter(),
                 font=("Arial", 16), wraplength=700, justify="left").pack(pady=20)
        tk.Label(self.root, text=f"A wild {self.current_enemy.name} appears!",
                 font=("Arial", 20)).pack(pady=20)

        tk.Button(self.root, text="Continue", font=("Arial", 14),
                  command=self.battle_screen).pack(pady=20)

    def battle_screen(self):
        self.clear_screen()
        enemy = self.current_enemy
        is_boss = self.is_boss_fight

        # --- Image mapping ---
        enemy_images = {
            "Mancubus": resource_path("assets/enemies/minion/mancubus.png"),
            "Caragor": resource_path("assets/enemies/minion/caragor.png"),
            "Nazgul": resource_path("assets/enemies/minion/nazgul.png")
        }
        boss_images = {
            "Mancubus": resource_path("assets/enemies/boss/boss_mancubus.png"),
            "Caragor": resource_path("assets/enemies/boss/boss_caragor.png"),
            "Nazgul": resource_path("assets/enemies/boss/boss_nazgul.png")
        }

        img_path = boss_images[self.game.first_enemy_choice] if is_boss \
            else enemy_images[enemy.name]
        img = Image.open(img_path).resize((800, 600))
        self.enemy_bg = ImageTk.PhotoImage(img)
        tk.Label(self.root, image=self.enemy_bg).place(x=0, y=0, relwidth=1, relheight=1)

        # --- Top info bar ---
        top_frame = tk.Frame(self.root, bg="black", height=40)
        top_frame.pack(fill="x", pady=5)

        self.player_hp_label = tk.Label(
            top_frame,
            text=f"{self.game.player.name} | HP: {self.game.player.health} | "
                 f"DMG: {self.game.player.damage} | Potions: {self.game.player.potions}",
            font=("Arial", 12), bg="black", fg="white"
        )
        self.player_hp_label.pack(side="left", padx=10)

        self.enemy_hp_label = tk.Label(
            top_frame,
            text=f"{enemy.name} | HP: {enemy.health} | DMG: {enemy.damage}",
            font=("Arial", 12), bg="black", fg="white"
        )
        self.enemy_hp_label.pack(side="right", padx=10)

        # --- Buttons ---
        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(side="bottom", pady=10)

        btn_width = 18
        tk.Button(button_frame, text="Attack", width=btn_width,
                  command=self.attack).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Use Potion", width=btn_width,
                  command=self.use_potion).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Flee", width=btn_width,
                  command=self.run_from_enemy).grid(row=0, column=2, padx=5)

        # --- Log ---
        self.log = tk.Label(
            self.root, text="", font=("Arial", 12),
            fg="white", bg="black", wraplength=760, justify="left"
        )
        self.log.pack(side="bottom", fill="x", pady=5)

    def attack(self):
        enemy = self.current_enemy
        msg = ""

        # ---------- PLAYER ATTACK ----------
        if hasattr(self.game.player, "attack_enemy"):
            result = self.game.player.attack_enemy(enemy)
            if isinstance(result, tuple):
                damage, attack_msg = result
            else:
                damage, attack_msg = result, f"You deal {result} damage."
            msg += f"{attack_msg}\n"
        else:
            damage_result = enemy.take_damage(self.game.player.damage)
            if self.is_boss_fight:
                damage, shield_triggered, thornmail_triggered = damage_result
                if shield_triggered:
                    msg += "🛡️ The Dark Lord shielded himself! No damage dealt.\n"
                else:
                    msg += f"You dealt {damage} damage.\n"

                if thornmail_triggered:
                    thorn_damage = 5
                    thorn_taken = self.game.player.take_damage(thorn_damage)
                    if isinstance(thorn_taken, tuple):
                        tdmg, tmsg = thorn_taken
                        msg += f"🪓 Thornmail reflects {tdmg} damage!\n"
                        if tmsg:
                            msg += f"{tmsg}\n"
                    else:
                        msg += f"🪓 Thornmail reflects {thorn_taken} damage!\n"
            else:
                damage = damage_result[0] if isinstance(damage_result, tuple) else damage_result
                msg += f"You dealt {damage} damage.\n"

        # ---------- ENEMY COUNTERATTACK ----------
        if enemy.is_alive():
            if self.is_boss_fight:
                boss_attack_result = enemy.boss_attack(self.game.player)
                if isinstance(boss_attack_result, tuple):
                    boss_dmg, lifesteal_msg = boss_attack_result
                    if isinstance(boss_dmg, tuple):
                        dmg, passive_msg = boss_dmg
                        msg += f"{enemy.name} hits you for {dmg} damage (Base DMG: {enemy.damage}).\n"
                        if passive_msg:
                            msg += f"{passive_msg}\n"
                    else:
                        msg += f"{enemy.name} hits you for {boss_dmg} damage (Base DMG: {enemy.damage}).\n"
                    if lifesteal_msg:
                        msg += f"{lifesteal_msg}\n"
                else:
                    msg += f"{enemy.name} hits you for {boss_attack_result} damage (Base DMG: {enemy.damage}).\n"
            else:
                damage_taken = self.game.player.take_damage(enemy.damage)
                if isinstance(damage_taken, tuple):
                    dmg, passive_msg = damage_taken
                    msg += f"{enemy.name} hits you for {dmg} damage (Base DMG: {enemy.damage}).\n"
                    if passive_msg:
                        msg += f"{passive_msg}\n"
                else:
                    msg += f"{enemy.name} hits you for {damage_taken} damage (Base DMG: {enemy.damage}).\n"

        # ---------- DEATH CHECKS ----------
        if self.game.player.health <= 0:
            msg += "💀 You have fallen in battle...\n"
            self.log.config(text=msg)
            self.root.after(1000, lambda: self.end_screen(False))
            return

        if not enemy.is_alive():
            msg += f"✅ You defeated {enemy.name}!\n"
            self.log.config(text=msg)
            self.root.after(2000, self.after_battle)
        else:
            self.log.config(text=msg)

        self.update_battle_status()

    def use_potion(self):
        self.game.player.use_potion()
        self.update_battle_status()

    def run_from_enemy(self):
        messagebox.showinfo("Run", "You ran away!")
        self.end_screen(False)

    def update_battle_status(self):
        self.player_hp_label.config(
            text=f"{self.game.player.name} | HP: {self.game.player.health} | "
                 f"DMG: {self.game.player.damage} | Potions: {self.game.player.potions}"
        )
        self.enemy_hp_label.config(
            text=f"{self.current_enemy.name} | HP: {self.current_enemy.health} | "
                 f"DMG: {self.current_enemy.damage}"
        )

    def after_battle(self):
        if not self.is_boss_fight:
            self.boss_intro()
        else:
            if self.current_enemy.is_alive():
                return  # Still fighting boss
            self.end_screen(True)

    # ---------- BOSS ----------
    def boss_intro(self):
        self.clear_screen()
        boss_type = self.game.first_enemy_choice
        self.current_enemy = self.game.create_boss(boss_type)
        self.is_boss_fight = True

        tk.Label(self.root, text=Narrative.second_encounter(),
                 font=("Arial", 16), wraplength=700, justify="left").pack(pady=20)
        tk.Label(self.root, text=f"The Dark Lord ({boss_type}) approaches!",
                 font=("Arial", 20), fg="red").pack(pady=20)

        # ✅ Show passive description
        tk.Label(self.root, text=self.current_enemy.passive_description,
                 font=("Arial", 14), fg="orange", wraplength=700).pack(pady=10)

        tk.Button(self.root, text="Continue", font=("Arial", 14),
                  command=self.battle_screen).pack(pady=20)

    # ---------- END SCREEN ----------
    def end_screen(self, won):
        self.clear_screen()
        if won:
            tk.Label(self.root, text=Narrative.endgame(),
                     font=("Arial", 16), wraplength=700, fg="green").pack(pady=20)
        else:
            tk.Label(self.root, text="The Dark Lord has defeated you...\nDarkness consumes the land.",
                     font=("Arial", 16), wraplength=700, fg="red").pack(pady=20)

        tk.Button(self.root, text="Play Again", command=self.intro_screen).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = RPGGUI(root)
    root.mainloop()
