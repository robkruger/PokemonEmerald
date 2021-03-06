import pygame
import numpy as np
import glob

from game.Event import Event
from graphics.Cell import Cell
from graphics.CellHolder import CellHolder
from mapmaker.pygame_textinput import TextInput


def key_is_down(key):
    keys = pygame.key.get_pressed()
    if keys[key]:
        return True
    return False


class MapMaker(object):

    def __init__(self, window_size, world_size: tuple, texture_select_size: tuple):
        pygame.init()
        self.screen = pygame.display.set_mode((window_size[0] + texture_select_size[0],
                                               window_size[1] + texture_select_size[1]))
        self.Running = True
        self.pressed = False
        self.grid_height, self.grid_width = world_size
        self.window_size = window_size
        self.tiles_holder = np.zeros(world_size[0] * world_size[1], dtype=object).reshape(world_size[0], world_size[1])
        self.sprite_group = pygame.sprite.Group()
        self.sprite_select_group = pygame.sprite.Group()
        self.cell_size_width = int(((window_size[0] - 30) / self.grid_width) + 0.5)
        self.cell_size_height = int(((window_size[1] - 30) / self.grid_height) + 0.5)
        self.cell_size = self.cell_size_width if self.cell_size_width < self.cell_size_height else self.cell_size_height
        self.offset_width = (window_size[0] - (self.grid_width * self.cell_size)) / 2
        self.offset_height = (window_size[1] - (self.grid_height * self.cell_size)) / 2
        print(self.offset_width, self.offset_height)
        self.offset = self.offset_width + self.offset_height
        self.texture_tiles_holder = np.zeros(int(texture_select_size[0] / 16) * int(window_size[1] / 16),
                                             dtype=object).reshape(int(texture_select_size[0] / 16),
                                                                   int(window_size[1] / 16))
        self.sprite_sheet = pygame.image.load('assets/interior.png').convert_alpha()
        self.sprite_sheet_rect = self.sprite_sheet.get_rect()
        self.sprite_sheet_rect.x = window_size[0]
        # self.sprite_select_group = pygame.sprite.Group(self.sprite_sheet)
        self.selection = (window_size[0], 0)
        self.grid_select_x = 0
        self.grid_select_y = 0
        self.select_x = 0
        self.select_y = 0
        self.load = False
        self.tiles = np.zeros(world_size[0] * world_size[1], dtype=object).reshape(world_size[0], world_size[1])
        self.texture_tiles = np.zeros(int(texture_select_size[0] / 16) * int(window_size[1] / 16),
                                      dtype=object).reshape(int(texture_select_size[0] / 16), int(window_size[1] / 16))
        self.left_pressed = False
        self.middle_pressed = False
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                self.tiles_holder[y][x] = (CellHolder(x, y, 1, 0, 16, self.cell_size / 16, self.offset_width,
                                                      self.offset_height, True, Event.NONE))

        # for tx in range(self.texture_tiles_holder.shape[0]):
        #     for ty in range(self.texture_tiles_holder.shape[1]):
        #         self.texture_tiles_holder[tx][ty] = (CellHolder(tx, ty, tx, ty, 16, 1, self.window_size[0], 0))

        for x in range(self.grid_width):
            for y in range(self.grid_height):
                c: CellHolder
                c = self.tiles_holder[y][x]
                self.tiles[y][x] = Cell(c.x, c.y, c.sheet_x, c.sheet_y, 16, self.cell_size / 16, self.offset_width,
                                        self.offset_height, self.sprite_group, self.sprite_sheet, c.movable, c.event)

        # for x in range(self.texture_tiles_holder.shape[0]):
        #     for y in range(self.texture_tiles_holder.shape[1]):
        #         c: CellHolder
        #         c = self.texture_tiles_holder[x][y]
        #         self.texture_tiles[x][y] = Cell(c.x,  c.y, c.sheet_x, c.sheet_y, c.size, c.scale, c.offset_w,
        #                                         c.offset_h, self.sprite_select_group, self.sprite_sheet)

        pygame.font.init()
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 35)
        self.frame_cooldown = 0
        self.frames = 0
        self.show_event = True
        self.show_sheet = True
        self.text_input = TextInput()
        self.pokemon_strings = []
        self.maps = []
        self.maps = glob.glob('./*.npz')
        self.current_map = 0
        self.switch = False

    def parse_events(self):
        self.frames += 1
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.Running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_CAPSLOCK:
                    self.load = True
                if event.key != pygame.K_CAPSLOCK:
                    self.load = False
                if event.key == pygame.K_TAB:
                    self.switch = True
                if event.key != pygame.K_TAB:
                    self.switch = False
                if pygame.key.get_mods() and pygame.KMOD_SHIFT:
                    self.show_event = not self.show_event
                if event.key == pygame.K_LCTRL:
                    self.show_sheet = not self.show_sheet
                if event.key == pygame.K_RETURN and not self.show_sheet:
                    self.pokemon_strings = np.append(self.pokemon_strings, str.split(self.text_input.get_text()))
                    self.text_input.clear_text()
                if event.key == pygame.K_DELETE and not self.show_sheet:
                    self.pokemon_strings = np.delete(self.pokemon_strings, len(self.pokemon_strings) - 1)
                    self.pokemon_strings = np.delete(self.pokemon_strings, len(self.pokemon_strings) - 1)
            else:
                self.load = False
                self.switch = False

        self.text_input.update(events)

    def draw(self):
        self.screen.fill((255, 255, 255))

        if pygame.mouse.get_pressed()[0]:
            self.pressed = True
        else:
            self.pressed = False

        if pygame.mouse.get_pressed()[1] and self.frame_cooldown + 40 < self.frames:
            self.frame_cooldown = self.frames
            self.middle_pressed = True
        else:
            self.middle_pressed = False

        if pygame.mouse.get_pressed()[2]:
            self.left_pressed = True
        else:
            self.left_pressed = False

        if key_is_down(pygame.K_ESCAPE):
            name = ''
            if len(glob.glob('./*.npz')) != len(self.maps):
                name = 'data' + str(len(self.maps) + 1)
            else:
                name = 'data' + str(self.current_map + 1)
            np.savez(name, self.tiles_holder, self.pokemon_strings)
            self.Running = False

        if self.switch:
            self.current_map = (self.current_map + 1) % len(self.maps)
            self.load = True

        if self.load:
            np_load_old = np.load
            np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)
            npzfile = np.load(self.maps[self.current_map])
            self.tiles_holder = npzfile['arr_0']
            self.pokemon_strings = npzfile['arr_1']
            np.load = np_load_old
            for x in range(self.tiles_holder.shape[0]):
                for y in range(self.tiles_holder.shape[1]):
                    c: CellHolder
                    c = self.tiles_holder[x][y]
                    self.tiles[x][y] = Cell(c.x, c.y, c.sheet_x, c.sheet_y, c.size, self.cell_size / 16,
                                            self.offset_width, self.offset_height, self.sprite_group, self.sprite_sheet,
                                            c.movable, c.event)

        self.grid_select_x = int((pygame.mouse.get_pos()[0] - self.offset_width) / self.cell_size)
        self.grid_select_y = int((pygame.mouse.get_pos()[1] - self.offset_height) / self.cell_size)

        # Calculate cell size based on the world size and window size
        self.cell_size_width = int(((self.window_size[0] - 30) / self.grid_width) + 0.5)
        self.cell_size_height = int(((self.window_size[1] - 30) / self.grid_height) + 0.5)
        self.cell_size = self.cell_size_width if self.cell_size_width < self.cell_size_height else self.cell_size_height
        self.offset_width = (self.window_size[0] - (self.grid_width * self.cell_size)) / 2
        self.offset_height = (self.window_size[1] - (self.grid_height * self.cell_size)) / 2

        # draw
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                pygame.draw.rect(self.screen, [0, 0, 0],
                                 [x * self.cell_size + self.offset_width, y * self.cell_size + self.offset_height,
                                  self.cell_size, self.cell_size], 1)

        self.sprite_group.draw(self.screen)

        # print([(self.selection[0] - self.window_size[0]) / 16, self.selection[1] / 16,
        #        self.cell_size, self.cell_size])

        if self.pressed and pygame.mouse.get_pos()[0] > self.window_size[0] and self.show_sheet:
            self.select_x = int((pygame.mouse.get_pos()[0] - self.window_size[0]) / 16)
            self.select_y = int(pygame.mouse.get_pos()[1] / 16)
            self.selection = (int((pygame.mouse.get_pos()[0]) / 16) * 16 + 8,
                              int(pygame.mouse.get_pos()[1] / 16) * 16)

        if self.pressed and pygame.mouse.get_pos()[0] < self.window_size[0]:
            self.tiles[self.grid_select_y][self.grid_select_x].kill()
            self.tiles_holder[self.grid_select_y][self.grid_select_x] = CellHolder(self.grid_select_x,
                                                                                   self.grid_select_y,
                                                                                   self.select_x,
                                                                                   self.select_y,
                                                                                   16, self.cell_size / 16,
                                                                                   self.offset_width,
                                                                                   self.offset_height,
                                                                                   True,
                                                                                   Event.NONE)
            c: CellHolder
            c = self.tiles_holder[self.grid_select_y][self.grid_select_x]
            self.tiles[self.grid_select_y][self.grid_select_x] = Cell(c.x, c.y, c.sheet_x, c.sheet_y, c.size,
                                                                      self.cell_size / 16, c.offset_w, c.offset_h,
                                                                      self.sprite_group, self.sprite_sheet, c.movable,
                                                                      c.event)

        if self.show_sheet:
            pygame.draw.rect(self.screen, [0, 0, 0], [self.selection[0], self.selection[1], 16, 16], 1)

        if self.left_pressed and pygame.mouse.get_pos()[0] < self.window_size[0]:
            c = self.tiles_holder[self.grid_select_y][self.grid_select_x]
            self.tiles_holder[self.grid_select_y][self.grid_select_x] = CellHolder(self.grid_select_x,
                                                                                   self.grid_select_y,
                                                                                   c.sheet_x,
                                                                                   c.sheet_y,
                                                                                   16, self.cell_size / 16,
                                                                                   self.offset_width,
                                                                                   self.offset_height,
                                                                                   not c.movable,
                                                                                   c.event)

        if self.middle_pressed and pygame.mouse.get_pos()[0] < self.window_size[0]:
            c = self.tiles_holder[self.grid_select_y][self.grid_select_x]
            self.tiles_holder[self.grid_select_y][self.grid_select_x] = CellHolder(self.grid_select_x,
                                                                                   self.grid_select_y,
                                                                                   c.sheet_x,
                                                                                   c.sheet_y,
                                                                                   16, self.cell_size / 16,
                                                                                   self.offset_width,
                                                                                   self.offset_height,
                                                                                   c.movable,
                                                                                   Event((c.event.value + 1) % 4))

        for x in range(self.tiles_holder.shape[0]):
            for y in range(self.tiles_holder.shape[1]):
                if not self.tiles_holder[x][y].movable:
                    self.draw_cross(
                        pygame.Rect((self.tiles_holder[x][y].x * self.cell_size + self.offset_width,
                                     self.tiles_holder[x][y].y * self.cell_size + self .offset_height),
                                    (self.cell_size, self.cell_size)))

        if self.show_event:
            for x in range(self.tiles_holder.shape[0]):
                for y in range(self.tiles_holder.shape[1]):
                    textsurface = self.font.render(str(self.tiles_holder[x][y].event.value), True, (255, 255, 255))
                    self.screen.blit(textsurface, (y * self.cell_size + 22 + self.offset_width,
                                                   x * self.cell_size + 15 + self.offset_height))

        if pygame.mouse.get_pos()[0] < self.window_size[0]:
            pygame.draw.rect(self.screen, [0, 0, 0],
                             [self.grid_select_x * self.cell_size + self.offset_width,
                              self.grid_select_y * self.cell_size + self.offset_height,
                              self.cell_size,
                              self.cell_size], 1)

        if self.show_sheet:
            self.screen.blit(self.sprite_sheet, self.sprite_sheet_rect)
        else:
            textsurface = self.font.render("Pokédex ID + Probability Percentage", True, (0, 0, 0))
            self.screen.blit(textsurface, (self.window_size[0], 0))
            i = 1
            for x in range(len(self.pokemon_strings)):
                if x % 2 == 1:
                    continue
                textsurface = self.font.render(str(self.pokemon_strings[x] + " " + self.pokemon_strings[x + 1]),
                                               True, (0, 0, 0))
                self.screen.blit(textsurface, (self.window_size[0], i * 30))
                i += 1
            self.screen.blit(self.text_input.get_surface(), (self.window_size[0], 30 * i))

        pygame.display.flip()

    def draw_cross(self, rect: pygame.Rect):
        pygame.draw.line(self.screen, (255, 0, 0), rect.bottomright, rect.topleft, 3)
        pygame.draw.line(self.screen, (255, 0, 0), rect.bottomleft, rect.topright, 3)

    @staticmethod
    def close():
        pygame.quit()
