class Pokemon(object):

    def __init__(self, name, id, moves: list, hp):
        self.name = name
        self.id = id
        self.moves = moves
        self.current_hp = hp
        self.max_hp = hp
