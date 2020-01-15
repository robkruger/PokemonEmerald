import math
import random


class Pokemon(object):

    def __init__(self, name, id, moves: list, level, base):
        self.name = name
        self.id = id
        self.moves = moves
        self.level = level
        self.base = base
        self.iv = random.randint(0, 31)
        self.hp_ev = 0
        self.attack_ev = 0
        self.defense_ev = 0
        self.sp_attack_ev = 0
        self.sp_defense_ev = 0
        self.speed_ev = 0
        self.total_ev = self.hp_ev + self.attack_ev + self.defense_ev + self.sp_attack_ev + self.defense_ev + self.speed_ev
        self.max_hp = math.floor((2 * base['HP'] + self.iv + (0 / 4) * level) / 100 + level + 10)
        self.current_hp = self.max_hp
        self.attack = math.floor((2 * self.base['Attack'] + self.iv + (self.attack_ev / 4) * level) / 100 + 5)  # * nature
        self.defense = math.floor((2 * self.base['Defense'] + self.iv + (self.defense_ev / 4) * level) / 100 + 5)  # * nature
        self.speed = math.floor((2 * self.base['Speed'] + self.iv + (self.speed_ev / 4) * level) / 100 + 5)  # * nature
        self.sp_attack = math.floor((2 * self.base['Sp. Attack'] + self.iv + (self.sp_attack_ev / 4) * level) / 100 + 5)  # * nature
        self.sp_defense = math.floor((2 * self.base['Sp. Defense'] + self.iv + (self.sp_defense_ev / 4) * level) / 100 + 5)  # * nature
