import json
import pokebase as pb


class Move(object):

    def __init__(self, name):
        self.name = name.replace('-', ' ').lower().capitalize()
        self.move: list
        self.move = []
        try:
            with open('assets/Pokemon/JSON/move/' + str(self.name) + '.json', mode='rb') as f:
                try:
                    self.move = json.load(f)
                except Exception as e:
                    print(e)
                pass
        except IOError:
            move = pb.move(self.name.replace(' ', '-').lower()).data()
            with open('assets/Pokemon/JSON/move/' + str(self.name) + '.json', 'a') as f:
                f.write('[')
                json.dump(move, f)
                f.write(']')
            with open('assets/Pokemon/JSON/move/' + str(self.name) + '.json', mode='rb') as f:
                try:
                    self.move = json.load(f)
                except Exception as e:
                    print(e)
                pass
        self.type = self.move[0]['type']['name'].capitalize()
        self.max_pp = self.move[0]['pp']
        self.current_pp = self.max_pp
        self.power = self.move[0]['power']
        self.category = self.move[0]['meta']['category']['name']
        self.move_class = self.move[0]['damage_class']['name']

    def get_value(self, first=None, second=None, third=None):
        if first:
            if second:
                if third:
                    return self.move[0][first][second][third]
                else:
                    return self.move[0][first][second]
            else:
                return self.move[0][first]
        else:
            return None
