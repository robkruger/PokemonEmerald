from game.BattleType import BattleType
from game.battle import Battle
from game.game import Game
from mapmaker.map_maker import MapMaker

# m = MapMaker((600, 1024), (10, 15), (2472, 0))
#
# while m.Running:
#     m.parse_events()
#     m.draw()
#
# m.close()

g = Game('data1.npz', (600, 400))
# g.Battling = True
# g.battle = Battle(BattleType.WILD, (600, 400), g, 1)

while g.Running:
    if g.in_building:
        if g.building.Running:
            g.building.parse_events()
            if g.building.Running:
                g.building.draw()
        else:
            g.building = None
            g.in_building = False
            g.player.set_anim(False, False, False, True)
    elif not g.Battling:
        g.parse_events()
        g.draw()
    else:
        g.parse_battle()

g.close()
