import os

class Narrative:
    BASE_PATH = os.path.join(os.path.dirname(__file__), "texts")

    @staticmethod
    def read_file(filename):
        filepath = os.path.join(Narrative.BASE_PATH, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return f"[Missing text: {filename}]"

    @staticmethod
    def intro():
        return Narrative.read_file("intro.txt")

    @staticmethod
    def class_select():
        return Narrative.read_file("ClassSelect.txt")

    @staticmethod
    def first_encounter():
        return Narrative.read_file("firstencounter.txt")

    @staticmethod
    def second_encounter():
        return Narrative.read_file("secondencounter.txt")

    @staticmethod
    def endgame():
        return Narrative.read_file("endgame.txt")

    @staticmethod
    def mage_stats():
        return Narrative.read_file("MageStat.txt")

    @staticmethod
    def rogue_stats():
        return Narrative.read_file("RogueStat.txt")

    @staticmethod
    def warrior_stats():
        return Narrative.read_file("WarStat.txt")
