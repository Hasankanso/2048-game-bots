

import asyncio
import pygame
from player import Command, Player


class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def get_next_move(self, game):
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    return Command.TO_LEFT
                elif event.key == pygame.K_RIGHT:
                    return Command.TO_RIGHT
                elif event.key == pygame.K_UP:
                    return Command.TO_UP
                elif event.key == pygame.K_DOWN:
                    return Command.TO_DOWN
                elif event.key == pygame.K_ESCAPE:
                    return Command.CLOSE
                elif event.key == pygame.K_r:
                    return Command.RESTART
                
            elif event.type == pygame.QUIT:
                    return Command.CLOSE