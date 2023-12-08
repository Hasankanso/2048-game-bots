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