import numpy
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
        self.font = pygame.font.Font('assets/font/pokemon-emerald-pro.ttf', 40)
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
        self.state = BattleState.START
        self.selection = 0
        self.currentText = []
        self.totalText = []
        self.text = ''
        self.set_repeat(True, 1, 0)

    def parse_events(self, ticks):
        self.frames += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Battling = False
                self.game.Running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.state is BattleState.WAITING:
                    if self.selection == 2:
                        self.selection = 0
                    elif self.selection == 3:
                        self.selection = 1
                elif event.key == pygame.K_RIGHT and self.state is BattleState.WAITING:
                    if self.selection == 0:
                        self.selection = 2
                    elif self.selection == 1:
                        self.selection = 3
                elif event.key == pygame.K_UP and self.state is BattleState.WAITING:
                    if self.selection == 1:
                        self.selection = 0
                    elif self.selection == 3:
                        self.selection = 2
                elif event.key == pygame.K_DOWN and self.state is BattleState.WAITING:
                    if self.selection == 0:
                        self.selection = 1
                    elif self.selection == 2:
                        self.selection = 3

        if len(self.totalText) == 0 and self.state is BattleState.START:
            text = "A wild Pokémon appeared!"
            self.totalText = []
            for c in text:
                self.totalText.append(c)

    def draw(self, delta):
        self.screen.fill((255, 255, 255))

        self.screen.blit(self.arena, (0, 0))
        if self.state is BattleState.WAITING or BattleState.START:
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

        if delta % 35 == 0:
            self.addText()

        self.drawText(self.text, (255, 255, 255), pygame.Rect(30, 295, 250, 300), self.font)

        pygame.display.flip()

    # draw some text into an area of a surface
    # automatically wraps words
    # returns any text that didn't get blitted
    def drawText(self, text, color, rect, font, aa=False, bkg=None):
        rect = pygame.Rect(rect)
        y = rect.top
        lineSpacing = -2

        # get the height of the font
        fontHeight = font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if bkg:
                image = font.render(text[:i], 1, color, bkg)
                shadow = font.render(text[:i], aa, (color[0] - 200, color[1] - 200, color[2] - 200), bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)
                shadow = font.render(text[:i], aa, (color[0] - 200, color[1] - 200, color[2] - 200))

            self.screen.blit(shadow, (rect.left + 2, y + 2))
            self.screen.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

        return text

    def addText(self):
        if len(self.currentText) == len(self.totalText):
            return

        self.currentText.append(self.totalText[len(self.currentText)])
        self.text = ''
        for c in self.currentText:
            self.text = self.text + c

    def set_repeat(self, enabled=True, interval=0, delay=0):
        if enabled:
            pygame.key.set_repeat(delay, interval)
        else:
            pygame.key.set_repeat()
