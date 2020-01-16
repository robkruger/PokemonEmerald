import math
import random
import pokebase as pb


class Pokemon(object):

    def __init__(self, name, id, moves: list, level):
        self.name = name
        self.id = id
        self.moves = moves
        self.level = level
        self.iv = random.randint(0, 31)
        self.hp_ev = 0
        self.attack_ev = 0
        self.defense_ev = 0
        self.sp_attack_ev = 0
        self.sp_defense_ev = 0
        self.speed_ev = 0
        self.total_ev = self.hp_ev + self.attack_ev + self.defense_ev + self.sp_attack_ev + self.defense_ev + self.speed_ev
        stats = pb.pokemon(id).stats
        stat = {'Speed': 0,
                'Sp. Defense': 1,
                'Sp. Attack': 2,
                'Defense': 3,
                'Attack': 4,
                'HP': 5}
        self.max_hp = math.floor((2 * stats[stat['HP']].base_stat + self.iv + (0 / 4) * level) / 100 + level + 10)
        self.current_hp = self.max_hp
        self.attack = math.floor((2 * stats[stat['Attack']].base_stat + self.iv + (self.attack_ev / 4) * level) / 100 + 5)  # * nature
        self.defense = math.floor((2 * stats[stat['Defense']].base_stat + self.iv + (self.defense_ev / 4) * level) / 100 + 5)  # * nature
        self.speed = math.floor((2 * stats[stat['Speed']].base_stat + self.iv + (self.speed_ev / 4) * level) / 100 + 5)  # * nature
        self.sp_attack = math.floor((2 * stats[stat['Sp. Attack']].base_stat + self.iv + (self.sp_attack_ev / 4) * level) / 100 + 5)  # * nature
        self.sp_defense = math.floor((2 * stats[stat['Sp. Defense']].base_stat + self.iv + (self.sp_defense_ev / 4) * level) / 100 + 5)  # * nature
        print(self.attack, self.defense, self.speed, self.sp_attack, self.sp_defense)
