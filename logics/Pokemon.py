class Pokemon(object):

    def __init__(self, name, id, moves: list, level, hp, base):
        self.name = name
        self.id = id
        self.moves = moves
        self.level = level
        self.current_hp = hp
        self.max_hp = hp
        self.base = base
