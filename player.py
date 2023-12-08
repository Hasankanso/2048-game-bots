from enum import Enum

class Command(Enum):
    TO_LEFT = 1
    TO_RIGHT = 2
    TO_UP = 3
    TO_DOWN = 4
    CLOSE = 5
    RESTART = 6


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def get_next_move(self, game):
        # Implement logic to return a Move enum based on the game state
        pass