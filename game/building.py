import numpy as np
import pygame

from game.BattleType import BattleType
from game.Event import Event
from game.battle import Battle
from graphics.Player import Player
from graphics.Cell import Cell
from graphics.CellHolder import CellHolder


class Building(object):
    def __init__(self, map_path, window_size: tuple, game):
        pygame.init()
        pygame.display.set_caption('Overworld')
        icon = pygame.image.load('assets/logo.png')
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((window_size[0], window_size[1]))
        self.window_size = window_size
        self.map = map_path
        self.Running = True
        self.Battling = False
        self.tiles_holder: np.array
        np_load_old = np.load
        np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)
        npzfile = np.load(map_path)
        self.tiles_holder = npzfile['arr_0']
        pokemon_strings_np = npzfile['arr_1']
        np.load = np_load_old
        self.pokemon_strings = []
        for x in range(len(pokemon_strings_np)):
            if x % 2 == 1:
                continue
            self.pokemon_strings.append((pokemon_strings_np[x], pokemon_strings_np[x + 1]))
        self.tiles = np.zeros(self.tiles_holder.shape, dtype=object)
        self.sprite_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.sprite_sheet = pygame.image.load('assets/interior.png').convert_alpha()
        self.player_sheet = pygame.image.load('assets/player.png').convert_alpha()
        self.player_sheet_rect = self.player_sheet.get_rect()
        self.cell_size = 37
        self.move_length = 300  # milliseconds
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.move_countdown = self.move_length
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.start_moving_left = False
        self.start_moving_right = False
        self.start_moving_up = False
        self.start_moving_down = False
        self.moving = self.moving_left or self.moving_right or self.moving_up or self.moving_down
        self.start_moving = self.start_moving_left or self.start_moving_right or self.start_moving_up \
                            or self.start_moving_down
        for x in range(self.tiles_holder.shape[0]):
            for y in range(self.tiles_holder.shape[1]):
                c: CellHolder
                c = self.tiles_holder[x][y]
                self.tiles[x][y] = Cell(c.x, c.y, c.sheet_x, c.sheet_y, 16, self.cell_size / 16, 22,
                                        15, self.sprite_group, self.sprite_sheet, c.movable, c.event)

        self.walk_up = [(15, 0), (15, 23), (15, 0), (15, 45)]
        self.walk_left = [(30, 0), (30, 23), (30, 0), (30, 45)]
        self.walk_down = [(0, 0), (0, 23), (0, 0), (0, 45)]
        # self.run_up = [(15, 66), (15, 88), (15, 110)]
        # self.player = Player(0, 0, 15, 0, (14, 21), self.cell_size / 16, 22, 15, self.cell_size, self.player_group,
        #                      self.player_sheet)
        self.player = Player(150, True, int(self.tiles_holder.shape[1] / 2), self.tiles_holder.shape[0] - 1, (14, 21),
                             self.cell_size / 16, self.cell_size, 22, 15,
                             self.player_sheet, self.player_group)
        self.starting_point = (int(self.tiles_holder.shape[1] / 2), self.tiles_holder.shape[0] - 1)
        self.player.add_frames_up(self.walk_up)
        self.player.add_frames_left(self.walk_left)
        self.player.add_frames_down(self.walk_down)
        self.anim_count = 0
        self.battle = None
        self.game = game
        self.carpet_group = pygame.sprite.Group()
        carpet1 = Cell(int(self.tiles_holder.shape[1] / 2) - 0.5, self.tiles_holder.shape[0] - 0.75, 10, 32, 16, self.cell_size / 16,
                       22, 15, self.carpet_group, self.sprite_sheet, True, 4)
        carpet2 = Cell(int(self.tiles_holder.shape[1] / 2) + 0.5, self.tiles_holder.shape[0] - 0.75, 11, 32, 16, self.cell_size / 16,
                       22, 15, self.carpet_group, self.sprite_sheet, True, 4)
        self.carpet = (carpet1, carpet2)

    def parse_events(self):
        self.clock.tick()
        self.delta_time = self.clock.get_time()
        self.player.update_a(self.delta_time)
        self.player.update_img()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.Running = False

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and not self.start_moving and not self.moving:
            if self.movable(self.player.x, self.player.y - 1):
                self.start_moving_up = True
            else:
                self.player.set_anim(True, False, False, False)
        elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and not self.start_moving and not self.moving:
            if self.player.x == self.starting_point[0] and self.player.y == self.starting_point[1]:
                self.Running = False
                return
            if self.movable(self.player.x, self.player.y + 1):
                self.start_moving_down = True
            else:
                self.player.set_anim(False, False, False, True)
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not self.start_moving and not self.moving:
            if self.movable(self.player.x - 1, self.player.y):
                self.start_moving_left = True
            else:
                self.player.set_anim(False, True, False, False)
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not self.start_moving and not self.moving:
            if self.movable(self.player.x + 1, self.player.y):
                self.start_moving_right = True
            else:
                self.player.set_anim(False, False, True, False)

        self.moving = self.moving_left or self.moving_right or self.moving_up or self.moving_down
        self.start_moving = self.start_moving_left or self.start_moving_right or self.start_moving_up \
                            or self.start_moving_down

        if self.start_moving_down:
            self.start_moving_down = False
            self.moving_down = True
        if self.start_moving_up:
            self.start_moving_up = False
            self.moving_up = True
        if self.start_moving_left:
            self.start_moving_left = False
            self.moving_left = True
        if self.start_moving_right:
            self.start_moving_right = False
            self.moving_right = True

        if self.moving_down:
            self.move_down()
            self.player.set_anim(False, False, False, True)
        elif self.moving_up:
            self.move_up()
            self.player.set_anim(True, False, False, False)
        elif self.moving_left:
            self.move_left()
            self.player.set_anim(False, True, False, False)
        elif self.moving_right:
            self.move_right()
            self.player.set_anim(False, False, True, False)

        if self.moving or self.start_moving:
            self.player.play()
        else:
            self.player.stop()

    def draw(self):
        self.screen.fill((255, 255, 255))

        self.sprite_group.draw(self.screen)
        self.carpet_group.draw(self.screen)
        self.player_group.draw(self.screen)

        pygame.display.flip()

    def move_up(self):
        if self.move_countdown < 0:
            self.moving_up = False
            self.move_countdown = self.move_length
            self.player.set_pos((int(round(self.player.x)), int(round(self.player.y))))
            return
        elif self.move_countdown - self.delta_time < 0:
            self.player.move((0, (-1 * (1000 / self.move_length)) *
                              (abs(self.move_countdown - self.delta_time) / 1000)))
            self.move_countdown -= self.delta_time
            return
        self.player.move((0, (-1 * (1000 / self.move_length)) * (self.delta_time / 1000)))
        self.move_countdown -= self.delta_time

    def move_down(self):
        if self.move_countdown < 0:
            self.moving_down = False
            self.move_countdown = self.move_length
            self.player.set_pos((int(round(self.player.x)), int(round(self.player.y))))
            return
        elif self.move_countdown - self.delta_time < 0:
            self.player.move((0, (1 * (1000 / self.move_length)) *
                              (abs(self.move_countdown - self.delta_time) / 1000)))
            self.move_countdown -= self.delta_time
            return
        self.player.move((0, (1 * (1000 / self.move_length)) * (self.delta_time / 1000)))
        self.move_countdown -= self.delta_time

    def move_left(self):
        if self.move_countdown < 0:
            self.moving_left = False
            self.move_countdown = self.move_length
            self.player.set_pos((int(round(self.player.x)), int(round(self.player.y))))
            return
        elif self.move_countdown - self.delta_time < 0:
            self.player.move(((-1 * (1000 / self.move_length)) *
                              (abs(self.move_countdown - self.delta_time) / 1000), 0))
            self.move_countdown -= self.delta_time
            return
        self.player.move(((-1 * (1000 / self.move_length)) * (self.delta_time / 1000), 0))
        self.move_countdown -= self.delta_time

    def move_right(self):
        if self.move_countdown < 0:
            self.moving_right = False
            self.move_countdown = self.move_length
            self.player.set_pos((int(round(self.player.x)), int(round(self.player.y))))
            return
        elif self.move_countdown - self.delta_time < 0:
            self.player.move(((1 * (1000 / self.move_length)) *
                              (abs(self.move_countdown - self.delta_time) / 1000), 0))
            self.move_countdown -= self.delta_time
            return
        self.player.move(((1 * (1000 / self.move_length)) * (self.delta_time / 1000), 0))
        self.move_countdown -= self.delta_time

    def event_handling(self, event):
        if event == Event.NONE:
            # Nothing
            return
        elif event == Event.GRASS:
            for p in self.pokemon_strings:
                if np.random.randint(1, (1000 / int(p[1]))) == 1:
                    print("Wild Pokemon! ", p[0], (1000 / int(p[1])), int(p[1]))
                    self.Battling = True
                    self.battle = Battle(BattleType.WILD, self.window_size, self, int(p[0]))
        elif event == Event.NPC:
            # TODO
            # Start battle with npc trainer
            return
        elif event == Event.DOOR:
            self.game.building = None
            self.game.in_building = False
            return

    def set_repeat(self, enabled=True, interval=0, delay=0):
        if enabled:
            pygame.key.set_repeat(delay, interval)
        else:
            pygame.key.set_repeat()

    def movable(self, x, y):
        if y >= np.size(self.tiles, 0) or y < 0:
            return False
        elif x >= np.size(self.tiles, 1) or x < 0:
            return False
        return self.tiles[y][x].movable

    @staticmethod
    def close():
        pygame.quit()
