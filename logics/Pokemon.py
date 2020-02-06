import json
import math
import random
import pokebase as pb

from logics.Move import Move


class Pokemon(object):

    def __init__(self, id, level):
        self.id = id
        self.level = level
        self.iv = random.randint(0, 31)
        self.hp_ev = 0
        self.attack_ev = 0
        self.defense_ev = 0
        self.sp_attack_ev = 0
        self.sp_defense_ev = 0
        self.speed_ev = 50
        self.total_ev = self.hp_ev + self.attack_ev + self.defense_ev + self.sp_attack_ev + self.defense_ev + self.speed_ev
        self.pokemon = []
        try:
            with open('assets/Pokemon/JSON/' + str(id) + '.json', mode='rb') as f:
                try:
                    self.pokemon = json.load(f)
                except Exception as e:
                    print(e)
                pass
        except IOError:
            pokemon = pb.pokemon(id)
            with open('assets/Pokemon/JSON/' + str(id) + '.json', 'a') as f:
                f.write('[')
                json.dump(pokemon.data(), f)
                f.write(']')
            with open('assets/Pokemon/JSON/' + str(id) + '.json', mode='rb') as f:
                try:
                    self.pokemon = json.load(f)
                except Exception as e:
                    print(e)
                pass
        self.stat = {'speed': 0,
                     'special-defense': 1,
                     'special-attack': 2,
                     'defense': 3,
                     'attack': 4,
                     'hp': 5}
        self.name = self.pokemon[0]['name'].capitalize()
        self.max_hp = math.floor((2 * self.get_stat('hp', 'base_stat') + self.iv + (0 / 4) * level) / 100 + level + 10)
        self.current_hp = self.max_hp
        self.attack = math.floor((2 * self.get_stat('attack', 'base_stat') + self.iv + (self.attack_ev / 4) * level) / 100 + 5)  # * nature
        self.defense = math.floor((2 * self.get_stat('defense', 'base_stat') + self.iv + (self.defense_ev / 4) * level) / 100 + 5)  # * nature
        self.speed = math.floor((2 * self.get_stat('speed', 'base_stat') + self.iv + (self.speed_ev / 4) * level) / 100 + 5)  # * nature
        self.sp_attack = math.floor((2 * self.get_stat('special-attack', 'base_stat') + self.iv + (self.sp_attack_ev / 4) * level) / 100 + 5)  # * nature
        self.sp_defense = math.floor((2 * self.get_stat('special-defense', 'base_stat') + self.iv + (self.sp_defense_ev / 4) * level) / 100 + 5)  # * nature
        self.mod_values = [0, 0, 0, 0, 0]
        self.moves = []
        print(self.name, self.speed)
        for move in self.pokemon[0]['moves']:
            i = 0
            for version in move['version_group_details']:
                if version['version_group']['name'] == "emerald":
                    if move['version_group_details'][i]['move_learn_method']['name'] == 'level-up':
                        if move['version_group_details'][i]['level_learned_at'] <= self.level:
                            self.moves.append(Move(move['move']['name']))
                i += 1

    def get_stat(self, stat_str, value):
        return self.pokemon[0]['stats'][self.stat[stat_str]][value]
