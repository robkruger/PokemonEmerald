from game.BattleType import BattleType
from game.battle import Battle
from game.game import Game
from mapmaker.map_maker import MapMaker

# m = MapMaker((600, 400), (10, 15), (1408, 0))
#
# while m.Running:
#     m.parse_events()
#     m.draw()
#
# m.close()

g = Game('data.npz', (600, 400))
g.Battling = True
g.battle = Battle(BattleType.WILD, (600, 400), g, 184)

while g.Running:
    if not g.Battling:
        g.parse_events()
        g.draw()
    else:
        g.parse_battle()

g.close()

