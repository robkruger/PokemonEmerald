import json
import math
import random
import pokebase as pb


class Pokemon(object):

    def __init__(self, id, moves: list, level):
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
        stats = []
        try:
            with open('assets/Pokemon/JSON/' + str(id) + '.json', mode='rb') as f:
                try:
                    stats = json.load(f)
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
                    stats = json.load(f)
                except Exception as e:
                    print(e)
                pass
        stat = {'Speed': 0,
                'Sp. Defense': 1,
                'Sp. Attack': 2,
                'Defense': 3,
                'Attack': 4,
                'HP': 5}
        self.name = stats[0]['name'].capitalize()
        self.max_hp = math.floor((2 * stats[0]['stats'][stat['HP']]['base_stat'] + self.iv + (0 / 4) * level) / 100 + level + 10)
        self.current_hp = self.max_hp
        self.attack = math.floor((2 * stats[0]['stats'][stat['Attack']]['base_stat'] + self.iv + (self.attack_ev / 4) * level) / 100 + 5)  # * nature
        self.defense = math.floor((2 * stats[0]['stats'][stat['Defense']]['base_stat'] + self.iv + (self.defense_ev / 4) * level) / 100 + 5)  # * nature
        self.speed = math.floor((2 * stats[0]['stats'][stat['Speed']]['base_stat'] + self.iv + (self.speed_ev / 4) * level) / 100 + 5)  # * nature
        self.sp_attack = math.floor((2 * stats[0]['stats'][stat['Sp. Attack']]['base_stat'] + self.iv + (self.sp_attack_ev / 4) * level) / 100 + 5)  # * nature
        self.sp_defense = math.floor((2 * stats[0]['stats'][stat['Sp. Defense']]['base_stat'] + self.iv + (self.sp_defense_ev / 4) * level) / 100 + 5)  # * nature
