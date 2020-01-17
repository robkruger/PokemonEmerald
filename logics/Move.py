import json
import pokebase as pb


class Move(object):

    def __init__(self, name):
        self.name = name
        move: list
        move = []
        try:
            with open('assets/Pokemon/JSON/move/' + str(self.name) + '.json', mode='rb') as f:
                try:
                    move = json.load(f)
                except Exception as e:
                    print(e)
                pass
        except IOError:
            move = pb.move(name.replace(' ', '-').lower()).data()
            with open('assets/Pokemon/JSON/move/' + str(self.name) + '.json', 'a') as f:
                f.write('[')
                json.dump(move, f)
                f.write(']')
            with open('assets/Pokemon/JSON/move/' + str(self.name) + '.json', mode='rb') as f:
                try:
                    move = json.load(f)
                except Exception as e:
                    print(e)
                pass
        move: dict
        self.type = move[0]['type']['name'].upper()
        self.pp = move[0]['pp']
        self.power = move[0]['power']
        self.category = move[0]['meta']['category']['name']
