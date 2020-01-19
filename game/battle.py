import pygame
import json
import math
import random
import pokebase as pb

from game.BattleType import BattleType
from game.BattleState import BattleState
from graphics.GIFImage import GIFImage
from logics.Move import Move
from logics.Pokemon import Pokemon
from PIL import Image


class Battle(object):
    def __init__(self, battle_type: BattleType, window_size: tuple, game, enemy_id):
        pygame.display.set_caption('Battle!')
        self.screen = pygame.display.set_mode((window_size[0], window_size[1]))
        self.type = battle_type
        self.Battling = True
        pygame.font.init()
        self.font = pygame.font.Font('assets/font/pokemon-emerald-pro.ttf', 40)
        self.game = game
        self.frames = 0
        self.arena = pygame.image.load('assets/UI/Arena.png').convert_alpha()
        decide_box_1 = pygame.image.load('assets/UI/Battle_1.png').convert_alpha()
        decide_box_2 = pygame.image.load('assets/UI/Battle_2.png').convert_alpha()
        decide_box_3 = pygame.image.load('assets/UI/Battle_3.png').convert_alpha()
        decide_box_4 = pygame.image.load('assets/UI/Battle_4.png').convert_alpha()
        move_box1 = pygame.image.load('assets/UI/Move_1.png').convert_alpha()
        move_box2 = pygame.image.load('assets/UI/Move_2.png').convert_alpha()
        move_box3 = pygame.image.load('assets/UI/Move_3.png').convert_alpha()
        move_box4 = pygame.image.load('assets/UI/Move_4.png').convert_alpha()
        turn_box = pygame.image.load('assets/UI/Turn.png').convert_alpha()
        friendly_box = pygame.image.load('assets/UI/FriendlyBox.png').convert_alpha()
        enemy_box = pygame.image.load('assets/UI/EnemyBox.png').convert_alpha()
        health_bar = pygame.image.load('assets/UI/health_bar.png').convert_alpha()
        self.pokemon_encounter = GIFImage('assets/Pokemon/Front/' + str(enemy_id) + '.gif', window_size)
        self.arena_scale = (int((window_size[0] / 240) * self.arena.get_rect().size[0]),
                            int((window_size[1] / 160) * self.arena.get_rect().size[1]))
        self.decide_box_scale = (int((window_size[0] / 240) * decide_box_1.get_rect().size[0]),
                                 int((window_size[1] / 160) * decide_box_1.get_rect().size[1]))
        self.move_box_scale = (int((window_size[0] / 240) * move_box1.get_rect().size[0]),
                               int((window_size[1] / 160) * move_box1.get_rect().size[1]))
        self.enemy_scale = (int((window_size[0] / 240)),
                            int((window_size[1] / 160)))
        self.friendly_box_scale = (int((window_size[0] / 240) * friendly_box.get_rect().size[0]),
                                   int((window_size[1] / 160) * friendly_box.get_rect().size[1]))
        self.enemy_box_scale = (int((window_size[0] / 240) * enemy_box.get_rect().size[0]),
                                int((window_size[1] / 160) * enemy_box.get_rect().size[1]))
        self.health_bar_scale = (int((window_size[0] / 240) * health_bar.get_rect().size[0]),
                                 int((window_size[1] / 160) * health_bar.get_rect().size[1]))
        decide_box_1 = pygame.transform.scale(decide_box_1, self.decide_box_scale)
        decide_box_2 = pygame.transform.scale(decide_box_2, self.decide_box_scale)
        decide_box_3 = pygame.transform.scale(decide_box_3, self.decide_box_scale)
        decide_box_4 = pygame.transform.scale(decide_box_4, self.decide_box_scale)
        move_box1 = pygame.transform.scale(move_box1, self.move_box_scale)
        move_box2 = pygame.transform.scale(move_box2, self.move_box_scale)
        move_box3 = pygame.transform.scale(move_box3, self.move_box_scale)
        move_box4 = pygame.transform.scale(move_box4, self.move_box_scale)
        friendly_box = pygame.transform.scale(friendly_box, self.friendly_box_scale)
        enemy_box = pygame.transform.scale(enemy_box, self.enemy_box_scale)
        turn_box = pygame.transform.scale(turn_box, self.move_box_scale)
        health_bar = pygame.transform.scale(health_bar, self.health_bar_scale)
        self.arena = pygame.transform.scale(self.arena, self.arena_scale)
        self.all_boxes = []
        self.all_boxes.append(decide_box_1)
        self.all_boxes.append(decide_box_2)
        self.all_boxes.append(decide_box_3)
        self.all_boxes.append(decide_box_4)
        self.all_boxes.append(move_box1)
        self.all_boxes.append(move_box2)
        self.all_boxes.append(move_box3)
        self.all_boxes.append(move_box4)
        self.all_boxes.append(health_bar)
        self.all_boxes.append(health_bar)
        self.all_boxes.append(friendly_box)
        self.all_boxes.append(enemy_box)
        self.all_boxes.append(turn_box)
        self.window_size = window_size
        self.state = BattleState.START
        self.selection = 0
        self.currentText = []
        self.totalText = []
        self.text = ''
        self.set_repeat(True, 1, 0)
        self.friendly_offset = 0
        self.last_offset = 0
        self.last_text = 0
        self.f_pokemon = Pokemon(102, 55)
        self.e_pokemon = Pokemon(enemy_id, 55)
        self.friendly_pokemon = pygame.image.load(
            'assets/Pokemon/Back/' + str(self.f_pokemon.id) + '.png').convert_alpha()
        self.friendly_pokemon = pygame.image.load('assets/Pokemon/Back/' + str(self.f_pokemon.id) + '.png')
        self.friendly_scale = (int((window_size[0] / 240) * self.friendly_pokemon.get_rect().size[0]),
                               int((window_size[1] / 160) * self.friendly_pokemon.get_rect().size[1]))
        self.friendly_pokemon = pygame.transform.scale(self.friendly_pokemon, self.friendly_scale)
        self.doneDamage = False
        self.enemyMove = None
        self.endBattle = False
        self.loser = None
        self.mod_table = {-6: 0.25,
                          -5: 0.28,
                          -4: 0.33,
                          -3: 0.4,
                          -2: 0.5,
                          -1: 0.66,
                           0: 1,
                           1: 1.5,
                           2: 2,
                           3: 2.5,
                           4: 3,
                           5: 3.5,
                           6: 4}
        self.stat = {'speed': 0,
                     'special-defense': 1,
                     'special-attack': 2,
                     'defense': 3,
                     'attack': 4,
                     'hp': 5}

    def parse_events(self, ticks):
        self.frames += 1
        enter_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Battling = False
                self.game.Running = False
            if event.type == pygame.KEYDOWN:
                moves = len(self.f_pokemon.moves)
                if event.key == pygame.K_LEFT and self.state is BattleState.WAITING:
                    if self.selection == 2:
                        self.selection = 0
                    elif self.selection == 3:
                        self.selection = 1
                    elif self.selection == 6:
                        self.selection = 4
                    elif self.selection == 7:
                        self.selection = 5
                elif event.key == pygame.K_RIGHT and self.state is BattleState.WAITING:
                    if self.selection == 0:
                        self.selection = 2
                    elif self.selection == 1:
                        self.selection = 3
                    elif self.selection == 4 and moves > 2:
                        self.selection = 6
                    elif self.selection == 5 and moves > 3:
                        self.selection = 7
                elif event.key == pygame.K_UP and self.state is BattleState.WAITING:
                    if self.selection == 1:
                        self.selection = 0
                    elif self.selection == 3:
                        self.selection = 2
                    elif self.selection == 5:
                        self.selection = 4
                    elif self.selection == 7:
                        self.selection = 6
                elif event.key == pygame.K_DOWN and self.state is BattleState.WAITING:
                    if self.selection == 0:
                        self.selection = 1
                    elif self.selection == 2:
                        self.selection = 3
                    elif self.selection == 4 and moves > 1:
                        self.selection = 5
                    elif self.selection == 6 and moves > 3:
                        self.selection = 7
                elif event.key == pygame.K_RETURN:
                    enter_pressed = True
                elif event.key == pygame.K_ESCAPE:
                    if self.selection == 4 or self.selection == 5 or self.selection == 6 or self.selection == 7:
                        self.selection = 0

        if len(self.currentText) == len(self.totalText) and self.endBattle and enter_pressed:
            self.game.Battling = False
        elif len(self.totalText) == 0 and self.state is BattleState.START:
            text = "A wild Pokémon appeared!"
            self.totalText = []
            for c in text:
                self.totalText.append(c)
        elif self.selection > 3 and self.state is BattleState.WAITING and enter_pressed:
            self.state = BattleState.FRIENDLY_TURN
            text = self.f_pokemon.name + " used " + str(self.f_pokemon.moves[self.selection - 4].name) + "!"
            self.totalText = []
            self.currentText = []
            self.text = ''
            for c in text:
                self.totalText.append(c)
        elif len(self.currentText) == len(self.totalText) and self.state is BattleState.FRIENDLY_TURN and enter_pressed:
            self.doneDamage = False
            self.doDamage(self.f_pokemon, self.e_pokemon, self.f_pokemon.moves[self.selection - 4])
        elif len(self.currentText) == len(self.totalText) \
                and self.state is BattleState.FRIENDLY_TURN and self.doneDamage:
            self.doneDamage = False
            if self.e_pokemon.current_hp == 0:
                self.endBattle = True
                self.loser = self.e_pokemon
                text = self.loser.name + " fainted!"
                self.currentText = []
                self.totalText = []
                for c in text:
                    self.totalText.append(c)
                return
            self.state = BattleState.ENEMY_TURN
            self.enemyMove = random.choice(self.e_pokemon.moves)
            text = self.e_pokemon.name + " used " + self.enemyMove.name + "!"
            self.totalText = []
            self.currentText = []
            self.text = ''
            for c in text:
                self.totalText.append(c)
        elif len(self.currentText) == len(self.totalText) \
                and self.state is BattleState.ENEMY_TURN and enter_pressed:
            self.doneDamage = False
            self.doDamage(self.e_pokemon, self.f_pokemon, self.enemyMove)
        elif self.selection == 0 and enter_pressed:
            self.selection = 4
        elif self.selection == 3 and enter_pressed:
            self.endBattle = True
            text = "Succesfully got away!"
            self.totalText = []
            self.currentText = []
            self.text = ''
            for c in text:
                self.totalText.append(c)
        elif len(self.currentText) == len(self.totalText) and (
                self.state is BattleState.START or BattleState.ENEMY_TURN) \
                and (enter_pressed or self.doneDamage):
            self.doneDamage = False
            self.selection = 0
            self.state = BattleState.WAITING
            text = "What will " + self.f_pokemon.name + " do?"
            self.totalText = []
            self.currentText = []
            self.text = ''
            for c in text:
                self.totalText.append(c)

    def draw(self, delta):
        self.screen.fill((255, 255, 255))

        self.screen.blit(self.arena, (0, 0))

        self.pokemon_encounter.render(self.screen,
                                      (int((430 - self.pokemon_encounter.get_width() * self.enemy_scale[0] / 2)
                                           * (self.window_size[0] / 600)),
                                       int((160 - self.pokemon_encounter.get_height() * self.enemy_scale[1])
                                           * (self.window_size[1] / 400))))
        self.screen.blit(self.friendly_pokemon, (int((150 - self.friendly_pokemon.get_rect().size[0] / 2)
                                                     * (self.window_size[0] / 600)),
                                                 int((281 + self.friendly_offset
                                                      - self.friendly_pokemon.get_rect().size[1])
                                                     * (self.window_size[1] / 400))))

        if self.state is BattleState.WAITING:
            if self.selection < 4:
                self.screen.blit(self.all_boxes[self.selection], (0, self.arena.get_rect().size[1]))
                self.drawText(self.text, (255, 255, 255), (55, 55, 55), pygame.Rect(30, 300, 250, 300), self.font)
            else:
                self.screen.blit(self.all_boxes[self.selection], (0, self.arena.get_rect().size[1]))
        elif self.state is BattleState.FRIENDLY_TURN or BattleState.ENEMY_TURN or BattleState.START:
            self.screen.blit(self.all_boxes[-1], (0, self.arena.get_rect().size[1]))
            self.drawText(self.text, (255, 255, 255), (55, 55, 55), pygame.Rect(30, 300, 550, 300), self.font)

        self.screen.blit(self.all_boxes[-3], (325 * (self.window_size[0] / 600), 185 * (self.window_size[1] / 400)))
        self.screen.blit(self.all_boxes[-2], (30 * (self.window_size[0] / 600), 40 * (self.window_size[1] / 400)))

        if delta - self.last_text >= 35:
            self.addText()
            self.last_text = delta

        if 500 <= delta - self.last_offset < 1000 and self.state is BattleState.WAITING:
            self.friendly_offset = -1
        elif delta - self.last_offset >= 1000 and self.state is BattleState.WAITING:
            self.friendly_offset = 0
            self.last_offset = delta

        if 3 < self.selection < 8 and self.state is BattleState.WAITING:
            moves = len(self.f_pokemon.moves)
            if moves > 0:
                self.drawText(self.f_pokemon.moves[0].name, (72, 72, 72), (208, 208, 200),
                              pygame.Rect(40, 23 + self.arena.get_rect().size[1], 300, 400), self.font, True)
            else:
                self.drawText('-', (72, 72, 72), (208, 208, 200),
                              pygame.Rect(40, 23 + self.arena.get_rect().size[1], 300, 400), self.font, True)
            if moves > 1:
                self.drawText(self.f_pokemon.moves[1].name, (72, 72, 72), (208, 208, 200),
                              pygame.Rect(40, 63 + self.arena.get_rect().size[1], 300, 400), self.font, True)
            else:
                self.drawText('-', (72, 72, 72), (208, 208, 200),
                              pygame.Rect(40, 63 + self.arena.get_rect().size[1], 300, 400), self.font, True)
            if moves > 2:
                self.drawText(self.f_pokemon.moves[2].name, (72, 72, 72), (208, 208, 200),
                              pygame.Rect(225, 23 + self.arena.get_rect().size[1], 300, 400), self.font, True)
            else:
                self.drawText('-', (72, 72, 72), (208, 208, 200),
                              pygame.Rect(225, 23 + self.arena.get_rect().size[1], 300, 400), self.font, True)
            if moves > 3:
                self.drawText(self.f_pokemon.moves[3].name, (72, 72, 72), (208, 208, 200),
                              pygame.Rect(225, 63 + self.arena.get_rect().size[1], 300, 400), self.font, True)
            else:
                self.drawText('-', (72, 72, 72), (208, 208, 200),
                              pygame.Rect(225, 63 + self.arena.get_rect().size[1], 300, 400), self.font, True)
            self.drawText("PP", (72, 72, 72), (208, 208, 200),
                          pygame.Rect(430, 22 + self.arena.get_rect().size[1], 300, 400), self.font, True)
            self.drawText(str(self.f_pokemon.moves[self.selection - 4].current_pp) + "/" + str(self.f_pokemon.moves[self.selection - 4].max_pp), (72, 72, 72),
                          (208, 208, 200),
                          pygame.Rect(505, 22 + self.arena.get_rect().size[1], 300, 400), self.font, True)
            self.drawText("TYPE/" + str(self.f_pokemon.moves[self.selection - 4].type), (72, 72, 72), (208, 208, 200),
                          pygame.Rect(430, 62 + self.arena.get_rect().size[1], 300, 400), self.font, True)

        temp_font = pygame.font.Font('assets/font/pokemon-emerald-pro.ttf', 28)
        self.drawText(str(self.f_pokemon.current_hp), (66, 66, 66), (222, 214, 181),
                      pygame.Rect(492, 238, 1000, 1000), temp_font)
        self.drawText("/", (66, 66, 66), (222, 214, 181),
                      pygame.Rect(514, 237, 1000, 1000), temp_font)
        self.drawText(str(self.f_pokemon.max_hp), (66, 66, 66), (222, 214, 181), pygame.Rect(540, 238, 1000, 1000),
                      temp_font)
        self.drawText(str(self.f_pokemon.name), (66, 66, 66), (222, 214, 181), pygame.Rect(367, 195, 1000, 1000),
                      temp_font)
        self.drawText("Lv" + str(self.f_pokemon.level), (66, 66, 66), (222, 214, 181),
                      pygame.Rect(510, 195, 1000, 1000),
                      temp_font)
        self.drawText(str(self.e_pokemon.name), (66, 66, 66), (222, 214, 181), pygame.Rect(43, 50, 1000, 1000),
                      temp_font)
        self.drawText("Lv" + str(self.e_pokemon.level), (66, 66, 66), (222, 214, 181),
                      pygame.Rect(195, 52, 1000, 1000),
                      temp_font)
        self.screen.blit(self.all_boxes[-5], (445 * (self.window_size[0] / 600), 228 * (self.window_size[1] / 400)))
        self.screen.blit(self.all_boxes[-4], (130 * (self.window_size[0] / 600), 83 * (self.window_size[1] / 400)))
        health_bar_scale_f = (int(self.health_bar_scale[0] * (self.f_pokemon.current_hp / self.f_pokemon.max_hp)),
                              self.health_bar_scale[1])
        health_bar_scale_e = (int(self.health_bar_scale[0] * (self.e_pokemon.current_hp / self.e_pokemon.max_hp)),
                              self.health_bar_scale[1])
        self.all_boxes[-5] = pygame.transform.scale(self.all_boxes[-5], health_bar_scale_f)
        self.all_boxes[-4] = pygame.transform.scale(self.all_boxes[-4], health_bar_scale_e)

        pygame.display.flip()

    def doDamage(self, user: Pokemon, target: Pokemon, move: Move):
        self.doneDamage = True
        if move.move_class == 'physical':
            level = user.level
            power = move.power
            a = user.attack * self.mod_table[user.mod_values[self.stat['attack']]]
            d = target.defense * self.mod_table[user.mod_values[self.stat['defense']]]
            damage = math.floor(math.floor(math.floor(2 * level / 5 + 2) * power * a / d) / 50 + 2)  # * modifier
            target.current_hp = max(target.current_hp - damage, 0)
        elif move.move_class == 'status':
            for stat_change in move.get_value('stat_changes'):
                target.mod_values[self.stat[stat_change['stat']['name']]] += stat_change['change']
        elif move.move_class == 'special':
            print('special')
        move.current_pp -= 1

    def drawText(self, text, color, shadow_color, rect, font: pygame.font.Font, scale=False):
        rect = pygame.Rect(rect)
        y = rect.top
        lineSpacing = -2

        fontHeight = font.size("Tg")[1]

        while text:
            i = 1

            if y + fontHeight > rect.bottom:
                break

            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1

            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            image = font.render(text[:i], False, color).convert_alpha()
            shadow = font.render(text[:i], False, shadow_color).convert_alpha()

            if scale:
                image = pygame.transform.smoothscale(image, (int(image.get_rect().size[0] * 0.9), image.get_rect().size[1]))
                shadow = pygame.transform.smoothscale(shadow, (int(shadow.get_rect().size[0] * 0.9), shadow.get_rect().size[1]))

            self.screen.blit(shadow, (rect.left + (self.window_size[0] / 240) * (fontHeight / 36),
                                      y + (self.window_size[1] / 160) * (fontHeight / 36)))
            self.screen.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing

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
