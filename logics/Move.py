import pokebase as pb

class Move(object):

    def __init__(self, name):
        self.name = name
        move = pb.move(name.replace(' ', '-').lower())
        self.type = move.type.name.upper()
        self.pp = move.pp
        self.power = move.power
        self.category = move.meta.category.name
        print(self.name, self.power, self.pp, self.type, self.category)
