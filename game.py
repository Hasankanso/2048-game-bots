# game.py
from player import Command, Player
from tile import Tile
from random import randrange, random
import numpy as np

class Game:
    def __init__(self, size : int = 4, winning_score : int = 2048):
        self.initialize_game(size)
        self.new_tiles_number = 2
        self.new_tiles(self.new_tiles_number)
        self.winning_score = winning_score

    def initialize_game(self, size: int = None):
        self.new_tiles_number = 2
        if(size is None):
            size = len(self.board)

        self.board = [[Tile(y, x, 0) for y in range(size)] for x in range(size)]
        self._score = 0

    def get_state(self):
       state = []
       for row in range(len(self.board)):
            for col in range(len(self.board)):
                state.append(self.board[row][col].normalize())
       return np.array(state)
    
    def is_game_over(self):
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                tile = self.board[row][col]
                if tile.value() >= self.winning_score:
                    return True
                if not tile.in_use():
                    return False
        return True

    def can_move_left(self):
        for row in range(len(self.board)):
            gap = False
            for col in range(len(self.board)):
                tile = self.board[row][col]
                if tile.in_use() and gap:
                    return True
                elif not tile.in_use():
                    gap = True
        return self.merge_left(True)

    def move_left(self, merge = True):
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                tile = self.board[row][col]
                if not tile.in_use():
                    other = self.find_next_used_tile_to_the_right(col, row)
                    if not other is None:
                        tile.swap_with(other)
        if merge:
            self.merge_left()

    def merge_left(self, dry_run = False):
        for row in range(len(self.board)):
            col = 0
            while col < len(self.board)-1:
                tile = self.board[row][col]
                if tile.in_use():
                    other = self.board[row][col+1]
                    if tile.equal_with(other):
                        if dry_run:
                            return True
                        tile.merge_with(other)
                        self._score += tile.value()
                        self.move_left(False)
                col += 1
        return False

    def can_move_right(self):
        for row in range(len(self.board)):
            gap = False
            for col in reversed(range(len(self.board))):
                tile = self.board[row][col]
                if tile.in_use() and gap:
                    return True
                elif not tile.in_use():
                    gap = True
        return self.merge_right(True)

    def move_right(self, merge = True):
        for row in range(len(self.board)):
            for col in reversed(range(len(self.board))):
                tile = self.board[row][col]
                if not tile.in_use():
                    other = self.find_next_used_tile_to_the_left(col, row)
                    if not other is None:
                        tile.swap_with(other)
        if merge:
            self.merge_right()

    def merge_right(self, dry_run = False):
        for row in range(len(self.board)):
            col = len(self.board)-1
            while col > 0:
                tile = self.board[row][col]
                if tile.in_use():
                    other = self.board[row][col-1]
                    if tile.equal_with(other):
                        if dry_run:
                            return True
                        tile.merge_with(other)
                        self._score += tile.value()
                        self.move_right(False)
                col -= 1
        return False

    def can_move_up(self):
        for col in range(len(self.board)):
            gap = False
            for row in range(len(self.board)):
                tile = self.board[row][col]
                if tile.in_use() and gap:
                    return True
                elif not tile.in_use():
                    gap = True
        return self.merge_up(True)

    def move_up(self, merge = True):
        for col in range(len(self.board)):
            for row in range(len(self.board)):
                tile = self.board[row][col]
                if not tile.in_use():
                    other = self.find_next_used_tile_to_the_bottom(col, row)
                    if not other is None:
                        tile.swap_with(other)
        if merge:
            self.merge_up()

    def merge_up(self, dry_run = False):
        for col in range(len(self.board)):
            row = 0
            while row < len(self.board)-1:
                tile = self.board[row][col]
                if tile.in_use():
                    other = self.board[row+1][col]
                    if tile.equal_with(other):
                        if dry_run:
                            return True
                        tile.merge_with(other)
                        self._score += tile.value()
                        self.move_up(False)
                row += 1
        return False

    def can_move_down(self):
        for col in range(len(self.board)):
            gap = False
            for row in reversed(range(len(self.board))):
                tile = self.board[row][col]
                if tile.in_use() and gap:
                    return True
                elif not tile.in_use():
                    gap = True
        return self.merge_down(True)

    def move_down(self, merge = True):
        for col in range(len(self.board)):
            for row in reversed(range(len(self.board))):
                tile = self.board[row][col]
                if not tile.in_use():
                    other = self.find_next_used_tile_to_the_top(col, row)
                    if not other is None:
                        tile.swap_with(other)
        if merge:
            self.merge_down()

    def merge_down(self, dry_run = False):
        for col in range(len(self.board)):
            row = len(self.board)-1
            while row > 0:
                tile = self.board[row][col]
                if tile.in_use():
                    other = self.board[row-1][col]
                    if tile.equal_with(other):
                        if dry_run:
                            return True
                        tile.merge_with(other)
                        self._score += tile.value()
                        self.move_down(False)
                row -= 1
        return False
    
    def step(self, command : Command):
        self.new_tiles_number = 0
        if command == Command.TO_LEFT and self.can_move_left():
            self.new_tiles_number = 1
            self.move_left()
        elif command == Command.TO_RIGHT and self.can_move_right():
            self.new_tiles_number = 1
            self.move_right()
        elif command == Command.TO_UP and self.can_move_up():
            self.new_tiles_number = 1
            self.move_up()
        elif command == Command.TO_DOWN and self.can_move_down():
            self.new_tiles_number = 1
            self.move_down()
        elif command == Command.CLOSE or self.is_game_over():
            self.new_tiles_number = 0
            self.running = False
        elif command == Command.RESTART:
            self.initialize_game()
        self.new_tiles(self.new_tiles_number)

    def get_score(self):
        return self._score

    def new_tile(self):
        # assuming is_game_over() == False :-)
        val = 2 if random() < 0.9 else 4
        i = 1
        while True:
            n = randrange(0, len(self.board) * len(self.board))
            row = int(n / len(self.board))
            col = len(self.board) if (n + 1) % len(self.board) == 0 else (n + 1) % len(self.board)
            col -= 1
            t = self.board[row][col]
            if not t.in_use():
                t.move(col, row)
                t.set_value(val)
                return

    def new_tiles(self, no : int):
        for i in range(0, no):
            self.new_tile()

    def find_next_used_tile_to_the_right(self, x : int, y : int):
        for i in range(x+1, len(self.board)):
            t = self.board[y][i]
            if t.in_use():
                return t

    def find_next_used_tile_to_the_left(self, x : int, y : int):
        for i in reversed(range(0, x)):
            t = self.board[y][i]
            if t.in_use():
                return t

    def find_next_used_tile_to_the_bottom(self, x : int, y : int):
        for i in range(y+1, len(self.board)):
            t = self.board[i][x]
            if t.in_use():
                return t

    def find_next_used_tile_to_the_top(self, x : int, y : int):
        for i in reversed(range(0, y)):
            t = self.board[i][x]
            if t.in_use():
                return t
