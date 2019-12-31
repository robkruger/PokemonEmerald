from game.game import Game
from mapmaker.map_maker import MapMaker

# m = MapMaker((600, 400), (10, 15), (1408, 0))
#
# while m.Running:
#     m.parse_events()
#     m.draw()
#
# m.close()

g = Game('data.npy', (600, 400))

while g.Running:
    g.parse_events()
    g.draw()

g.close()

