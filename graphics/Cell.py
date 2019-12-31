import pygame


class Cell(pygame.sprite.Sprite):

    def __init__(self, x, y, sheet_x, sheet_y, size, scale, offset_w, offset_h, group, sprite_sheet):
        pygame.sprite.Sprite.__init__(self, group)

        rect = pygame.Rect((sheet_x * size, sheet_y * size, size, size))
        self.image = pygame.Surface(rect.size).convert()
        self.image.blit(sprite_sheet, (0, 0), rect)
        self.image = pygame.transform.scale(self.image, (int(size * scale + 0.5), int(size * scale + 0.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x * size * scale + offset_w
        self.rect.y = y * size * scale + offset_h

    def kill(self):
        pygame.sprite.Sprite.kill(self)
