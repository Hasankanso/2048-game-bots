# game.py
from player import Player
from tile import Tile

class Game:
    def __init__(self, player : Player, size : int = 4):
        self.player = player
        self.initialize_game(size)


    def initialize_game(self, size: int = None):
        if(size is None):
            size = len(self.board)

        self.board = [[Tile(x, y, 0) for y in range(size)] for x in range(size)]
        self._score = 0

    def is_game_over(self):
        pass

    def move_left(self):
        #replace
        tile = self.board[0][0]
        tile.number = 1

    def move_right(self):
        #replace
        tile = self.board[0][0]
        tile.number = 2

    def move_up(self):
        #replace
        tile = self.board[0][0]
        tile.number = 3

    def move_down(self):
        #replace
        tile = self.board[0][0]
        tile.number = 4

    def get_score(self):
        return self._score