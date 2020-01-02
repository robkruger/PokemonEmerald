import pygame

from game.BattleType import BattleType


class Battle(object):
    def __init__(self, battle_type: BattleType, window_size: tuple):
        self.screen = pygame.display.set_mode((window_size[0], window_size[1]))
        self.type = battle_type
        self.Battling = True
        pygame.font.init()
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 35)

    def parse_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Battling = False

    def draw(self):
        self.screen.fill((255, 255, 255))

        textsurface = self.font.render("Battle!", True, (0, 0, 0))
        self.screen.blit(textsurface, (0, 0))

        pygame.display.flip()
