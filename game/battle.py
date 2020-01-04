import pygame

from game.BattleType import BattleType
from graphics.GIFImage import GIFImage


class Battle(object):
    def __init__(self, battle_type: BattleType, window_size: tuple, game):
        self.screen = pygame.display.set_mode((window_size[0], window_size[1]))
        self.type = battle_type
        self.Battling = True
        pygame.font.init()
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 35)
        self.game = game
        self.frames = 0
        self.arena = pygame.image.load('assets/UI/Arena.png').convert_alpha()
        self.arena = pygame.transform.scale(self.arena, (int((window_size[0] / 240) * self.arena.get_rect().size[0]),
                                                         int((window_size[1] / 160) * self.arena.get_rect().size[1])))
        self.decide_box = pygame.image.load('assets/UI/Battle_1.png').convert_alpha()
        self.decide_box = pygame.transform.scale(self.decide_box,
                                                 (int((window_size[0] / 240) * self.decide_box.get_rect().size[0]),
                                                  int((window_size[1] / 160) * self.decide_box.get_rect().size[1])))
        self.pokemon1 = GIFImage('assets/Pokemon/1.gif', window_size)
        self.window_size = window_size

    def parse_events(self, delta):
        self.frames += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Battling = False
                self.game.Running = False

    def draw(self, delta):
        self.screen.fill((255, 255, 255))

        self.screen.blit(self.arena, (0, 0))
        self.screen.blit(self.decide_box, (0, self.arena.get_rect().size[1]))
        self.pokemon1.render(self.screen, (int(375 * (self.window_size[0] / 600)),
                                           int(65 * (self.window_size[1] / 400))))

        pygame.display.flip()
