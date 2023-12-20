
from game_ui import GameUI
from genetic_bot import GeneticAlgorithm
from human_player import HumanPlayer

if __name__ == "__main__":
    #game = GameUI(player=HumanPlayer("Salah"))
    #game.run()

    algo = GeneticAlgorithm()
    algo.train()

