# tile.py

from colors import TileColor


class Tile:
    def __init__(self, x, y, number):
        self.x = x
        self.y = y
        self.number = number
        self.color : TileColor = TileColor.tileToColor(self)

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.color : TileColor = TileColor.tileToColor(self)

    def value(self):
        return self.number
    
    def set_value(self, val : int):
        self.number = val

    def in_use(self):
        return self.number > 0

    def swap_with(self, other):
        v = other.number
        other.number = self.number
        self.number = v

    def merge_with(self, other):
        # the check for equality happens outside
        self.number *= 2
        other.set_value(0)

    def equal_with(self, other):
        return self.number == other.number
