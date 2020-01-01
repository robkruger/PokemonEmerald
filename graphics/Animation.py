import pygame


class Animation(pygame.sprite.Sprite):
    def __init__(self, frame_time, looping, x, y, size, scale, cell_size, offset_w, offset_h, sprite_sheet, group):
        pygame.sprite.Sprite.__init__(self, group)

        rect = pygame.Rect((0, 0, size[0], size[1]))
        self.image = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.image.blit(sprite_sheet, (0, 0), rect)
        self.image = pygame.transform.scale(self.image, (int(size[0] * scale + 4), int(size[1] * scale)))
        self.rect = self.image.get_rect()
        self.rect.x = x * 16 * scale + offset_w
        self.rect.y = y * 16 * scale + offset_h - int(cell_size / 2 + 0.5)
        self.current_time = 0
        self.frame_time = frame_time
        self.frames_up = []
        self.frames_left = []
        self.frames_down = []
        self.current_frame = 0
        self.looping = looping
        self.playing = True
        self.size = size
        self.sprite_sheet = sprite_sheet
        self.cell_size = cell_size
        self.x = x
        self.y = y
        self.offset_w = offset_w
        self.offset_h = offset_h
        self.scale = scale
        self.up = True
        self.down = False
        self.left = False
        self.right = False

    def add_frames_up(self, frames):
        for frame in frames:
            self.frames_up.append((frame[0], frame[1]))

    def add_frames_left(self, frames):
        for frame in frames:
            self.frames_left.append((frame[0], frame[1]))

    def add_frames_down(self, frames):
        for frame in frames:
            self.frames_down.append((frame[0], frame[1]))

    def set_anim(self, up, left, right, down):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    def stop(self):
        self.playing = False
        if self.current_frame == 1:
            self.current_frame = 2
        elif self.current_frame == 3:
            self.current_frame = 0

    def play(self):
        self.playing = True

    def update_a(self, delta):
        if not self.playing:
            return
        self.current_time += delta
        if self.current_time > self.frame_time:
            self.current_time = self.current_time % self.frame_time
            if self.looping:
                self.current_frame = (self.current_frame + 1) % 4
            elif self.current_frame + 1 > 4:
                self.playing = False
            else:
                self.current_frame += 1

    def update_img(self):
        rect = pygame.Rect((0, 0, 0, 0))
        if self.up:
            rect = pygame.Rect((self.frames_up[self.current_frame][0], self.frames_up[self.current_frame][1],
                                self.size[0], self.size[1]))
        elif self.down:
            rect = pygame.Rect((self.frames_down[self.current_frame][0], self.frames_down[self.current_frame][1],
                                self.size[0], self.size[1]))
        elif self.left:
            rect = pygame.Rect((self.frames_left[self.current_frame][0], self.frames_left[self.current_frame][1],
                                self.size[0], self.size[1]))
        elif self.right:
            rect = pygame.Rect((self.frames_left[self.current_frame][0], self.frames_left[self.current_frame][1],
                                self.size[0], self.size[1]))

        self.image = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.image.blit(self.sprite_sheet, (0, 0), rect)
        self.image = pygame.transform.scale(self.image, (int(self.size[0] * self.scale + 4),
                                                         int(self.size[1] * self.scale)))
        if self.right:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = self.x * 16 * self.scale + self.offset_w
        self.rect.y = self.y * 16 * self.scale + self.offset_h - int(self.cell_size / 2 + 0.5)

    def reset(self):
        self.current_frame = 0

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