import pygame

from game.BattleType import BattleType
from game.BattleState import BattleState
from graphics.GIFImage import GIFImage


class Battle(object):
    def __init__(self, battle_type: BattleType, window_size: tuple, game, enemy_id):
        self.screen = pygame.display.set_mode((window_size[0], window_size[1]))
        self.type = battle_type
        self.Battling = True
        pygame.font.init()
        self.font = pygame.font.Font('assets/font/pokemon-emerald-pro.ttf', 50)
        self.game = game
        self.frames = 0
        self.arena = pygame.image.load('assets/UI/Arena.png').convert_alpha()
        self.decide_box_1 = pygame.image.load('assets/UI/Battle_1.png').convert_alpha()
        self.decide_box_2 = pygame.image.load('assets/UI/Battle_2.png').convert_alpha()
        self.decide_box_3 = pygame.image.load('assets/UI/Battle_3.png').convert_alpha()
        self.decide_box_4 = pygame.image.load('assets/UI/Battle_4.png').convert_alpha()
        self.turn_text_box = pygame.image.load('assets/UI/turn.png').convert_alpha()
        self.pokemon_encounter = GIFImage('assets/Pokemon/Front/' + str(enemy_id) + '.gif', window_size)
        self.friendly_pokemon = pygame.image.load('assets/Pokemon/Back/1.png').convert_alpha()
        self.arena_scale = (int((window_size[0] / 240) * self.arena.get_rect().size[0]),
                            int((window_size[1] / 160) * self.arena.get_rect().size[1]))
        self.decide_box_scale = (int((window_size[0] / 240) * self.decide_box_1.get_rect().size[0]),
                                 int((window_size[1] / 160) * self.decide_box_1.get_rect().size[1]))
        self.turn_box_scale = (int((window_size[0] / 240) * self.turn_text_box.get_rect().size[0]),
                               int((window_size[1] / 160) * self.turn_text_box.get_rect().size[1]))
        self.enemy_scale = (int((window_size[0] / 240)),
                            int((window_size[1] / 160)))
        self.friendly_scale = (int((window_size[0] / 240) * self.friendly_pokemon.get_rect().size[0]),
                               int((window_size[1] / 160) * self.friendly_pokemon.get_rect().size[1]))
        self.friendly_pokemon = pygame.transform.scale(self.friendly_pokemon, self.friendly_scale)
        self.decide_box_1 = pygame.transform.scale(self.decide_box_1, self.decide_box_scale)
        self.decide_box_2 = pygame.transform.scale(self.decide_box_2, self.decide_box_scale)
        self.decide_box_3 = pygame.transform.scale(self.decide_box_3, self.decide_box_scale)
        self.decide_box_4 = pygame.transform.scale(self.decide_box_4, self.decide_box_scale)
        self.turn_text_box = pygame.transform.scale(self.turn_text_box, self.turn_box_scale)
        self.arena = pygame.transform.scale(self.arena, self.arena_scale)
        self.window_size = window_size
        self.state = BattleState.WAITING
        self.selection = 0
        self.set_repeat(True, 1, 0)

    def parse_events(self, delta):
        self.frames += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Battling = False
                self.game.Running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.selection == 2:
                        self.selection = 0
                    elif self.selection == 3:
                        self.selection = 1
                elif event.key == pygame.K_RIGHT:
                    if self.selection == 0:
                        self.selection = 2
                    elif self.selection == 1:
                        self.selection = 3
                elif event.key == pygame.K_UP:
                    if self.selection == 1:
                        self.selection = 0
                    elif self.selection == 3:
                        self.selection = 2
                elif event.key == pygame.K_DOWN:
                    if self.selection == 0:
                        self.selection = 1
                    elif self.selection == 2:
                        self.selection = 3

    def draw(self, delta):
        self.screen.fill((255, 255, 255))

        self.screen.blit(self.arena, (0, 0))
        if self.state is BattleState.WAITING:
            if self.selection == 0:
                self.screen.blit(self.decide_box_1, (0, self.arena.get_rect().size[1]))
            elif self.selection == 1:
                self.screen.blit(self.decide_box_2, (0, self.arena.get_rect().size[1]))
            elif self.selection == 2:
                self.screen.blit(self.decide_box_3, (0, self.arena.get_rect().size[1]))
            elif self.selection == 3:
                self.screen.blit(self.decide_box_4, (0, self.arena.get_rect().size[1]))
        elif self.state is BattleState.FRIENDLY_TURN or self.state is BattleState.ENEMY_TURN:
            self.screen.blit(self.turn_text_box, (0, self.arena.get_rect().size[1]))
        self.pokemon_encounter.render(self.screen, (int((430 - self.pokemon_encounter.get_width() * self.enemy_scale[0] / 2)
                                                        * (self.window_size[0] / 600)),
                                                    int((160 - self.pokemon_encounter.get_height() * self.enemy_scale[1])
                                                        * (self.window_size[1] / 400))))
        self.screen.blit(self.friendly_pokemon, (int(70 * (self.window_size[0] / 600)),
                                                 int(160 * (self.window_size[1] / 400))))

        textsurface = self.font.render("Test", True, (255, 255, 255))
        self.screen.blit(textsurface, (30, 290))

        pygame.display.flip()

    def set_repeat(self, enabled=True, interval=0, delay=0):
        if enabled:
            pygame.key.set_repeat(delay, interval)
        else:
            pygame.key.set_repeat()
