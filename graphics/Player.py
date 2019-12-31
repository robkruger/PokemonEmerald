import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet_x, sheet_y, size, scale, offset_w, offset_h, cell_size, group, sprite_sheet):
        pygame.sprite.Sprite.__init__(self, group)

        rect = pygame.Rect((sheet_x, sheet_y, size[0], size[1]))
        self.image = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.image.blit(sprite_sheet, (0, 0), rect)
        self.image = pygame.transform.scale(self.image, (int(size[0] * scale + 4), int(size[1] * scale + 0.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x * 16 * scale + offset_w
        self.rect.y = y * 16 * scale + offset_h - int(cell_size / 2 + 0.5)
        self.x = x
        self.y = y
        self.scale = scale
        self.offset_w = offset_w
        self.offset_h = offset_h
        self.cell_size = cell_size
        self.size = size
        self.sprite_sheet = sprite_sheet

    def move(self, offset: tuple):
        self.x += offset[0]
        self.y += offset[1]
        self.rect.x = self.x * 16 * self.scale + self.offset_w
        self.rect.y = self.y * 16 * self.scale + self.offset_h - int(self.cell_size / 2 + 0.5)

    def set_pos(self, pos: tuple):
        self.x = pos[0]
        self.y = pos[1]
        self.rect.x = self.x * 16 * self.scale + self.offset_w
        self.rect.y = self.y * 16 * self.scale + self.offset_h - int(self.cell_size / 2 + 0.5)

    def set_frame(self, sheet: tuple, size: tuple):
        rect = pygame.Rect((sheet[0], sheet[1], size[0], size[1]))
        self.image = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.image.blit(self.sprite_sheet, (0, 0), rect)
        self.image = pygame.transform.scale(self.image, (int(self.size[0] * self.scale + 4), int(self.size[1] * self.scale + 0.5)))
        self.rect = self.image.get_rect()
        self.rect.x = self.x * 16 * self.scale + self.offset_w
        self.rect.y = self.y * 16 * self.scale + self.offset_h - int(self.cell_size / 2 + 0.5)

    def kill(self):
        pygame.sprite.Sprite.kill(self)