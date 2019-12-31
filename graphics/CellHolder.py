class CellHolder(object):
    def __init__(self, x, y, sheet_x, sheet_y, size, scale, offset_w, offset_h, movable):
        self.x = x
        self.y = y
        self.sheet_x = sheet_x
        self.sheet_y = sheet_y
        self.size = size
        self.scale: float
        self.scale = scale,
        self.offset_w = offset_w
        self.offset_h = offset_h
        self.movable = movable
