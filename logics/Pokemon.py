import math


class Pokemon(object):

    def __init__(self, name, id, moves: list, level, base):
        self.name = name
        self.id = id
        self.moves = moves
        self.level = level
        self.base = base
        # TODO
        # iv     ev
        # 0 and (0 / 4)
        self.max_hp = math.floor((2 * base['HP'] + 0 + (0 / 4) * level) / 100 + level + 10)
        self.current_hp = self.max_hp
        self.attack = math.floor((2 * self.base['Attack'] + 0 + (0 / 4) * level) / 100 + 5)  # * nature
        self.defense = math.floor((2 * self.base['Defense'] + 0 + (0 / 4) * level) / 100 + 5)  # * nature
        self.speed = math.floor((2 * self.base['Speed'] + 0 + (0 / 4) * level) / 100 + 5)  # * nature
        self.sp_attack = math.floor((2 * self.base['Sp. Attack'] + 0 + (0 / 4) * level) / 100 + 5)  # * nature
        self.sp_defense = math.floor((2 * self.base['Sp. Defense'] + 0 + (0 / 4) * level) / 100 + 5)  # * nature
        print(self.max_hp, self.attack, self.defense, self.speed, self.sp_attack, self.sp_defense)
