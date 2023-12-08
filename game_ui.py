# game_ui.py
import pygame
from game import Game
from player import Command, Player
import threading

class GameUI(Game):
    def __init__(self, player: Player, board_size: int = 6):
        super().__init__(player, board_size)
        pygame.init()
        self.top_offset = 150
        self.gap_size = 10
        self.gaps_total_size = self.gap_size*(len(self.board) + 1)
        self.screen_size = 100*len(self.board)
        self.screen = pygame.display.set_mode((self.screen_size + self.gaps_total_size, self.screen_size + self.gaps_total_size + self.top_offset))
        self.screen.fill((187,173,161))
        pygame.display.set_caption("My Game")

        self.clock = pygame.time.Clock()
        self.tile_size = (self.screen.get_size()[0] - self.gaps_total_size)/len(self.board)  # Size of each tile
        self.get_input_task = None
        self.running = True
        self.font = pygame.font.Font(None, 36)

    def draw_player_name(self):

        playerWord = self.font.render("Player", True, (119, 110, 102))
        word_rect = playerWord.get_rect(center=(50, 20))
        self.screen.blit(playerWord, word_rect)
        playerWord = self.font.render(self.player.name, True, (119, 110, 102))
        word_rect = playerWord.get_rect(center=(50, 50))
        self.screen.blit(playerWord, word_rect)

    def draw_score(self):
        scoreWord = self.font.render("SCORE", True, (119, 110, 102))
        word_rect = scoreWord.get_rect(center=(self.screen.get_size()[0] - 60, 20))
        self.screen.blit(scoreWord, word_rect)

        scoreNum = self.font.render(str(self.get_score()), True, (119, 110, 102))
        text_rect = scoreNum.get_rect(center=(self.screen.get_size()[0]- 60, 50))
        self.screen.blit(scoreNum, text_rect)

    def draw_board(self):
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                tile = self.board[row][col]
                if tile:
                    tile_pos = (self.gap_size + col * (self.tile_size + self.gap_size), self.top_offset + (self.tile_size + self.gap_size)*row + self.gap_size, self.tile_size, self.tile_size)
                    pygame.draw.rect(self.screen, (255, 204, 153), tile_pos)

                    if tile.number == 0:
                        numberText = ""
                    else:
                        numberText = str(tile.number)
                    
                    text = self.font.render(numberText, True, (119, 110, 102))
                    text_rect = text.get_rect(center=(tile_pos[0] + self.tile_size / 2, tile_pos[1] + self.tile_size / 2))
                    self.screen.blit(text, text_rect)

    def receive_player_action(self):
        while self.running:
            command = self.player.get_next_move(self)
            if command == Command.TO_LEFT:
                self.move_left()
            elif command == Command.TO_RIGHT:
                self.move_right()
            elif command == Command.TO_UP:
                self.move_up()
            elif command == Command.TO_DOWN:
                self.move_down()
            elif command == Command.CLOSE:
                self.running = False
            elif command == Command.RESTART:
                self.initialize_game()

    def run(self):
        input_thread = threading.Thread(target=self.receive_player_action, args=())
        input_thread.start()
        while self.running:
            self.draw_player_name()     
            self.draw_score()
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()
