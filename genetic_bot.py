import numpy as np
from game import Game

from player import Command, Player
import random


class GeneticBot(Player):

    def __init__(self, w_input_hidden, bias_hidden, w_hidden_output, bias_output):
        self.w_input_hidden = w_input_hidden
        self.bias_hidden = bias_hidden
        self.w_hidden_output = w_hidden_output
        self.bias_output = bias_output
        self.num_actions = 4
    def get_next_move(self, game : Game):
        input_data = game.get_state()
        outputs = self.forward(input_data, self.w_input_hidden, self.bias_hidden, self.w_hidden_output, self.bias_output)
        
        # Apply softmax to the action logits to get action probabilities
        action_probs = softmax(outputs[0])
        # Choose an action based on action probabilities (e.g., using softmax)
        action = np.random.choice(self.num_actions, p=action_probs.ravel())

        command = Command(action + 1)
        return command
    
    def get_neural_network(self):
        return self.w_input_hidden, self.bias_hidden, self.w_hidden_output, self.bias_output
    
    # Forward pass through the neural network
    def forward(self, input_data, weights_input_hidden, bias_hidden, weights_hidden_output, bias_output):
        hidden_layer_input = np.dot(input_data, weights_input_hidden) + bias_hidden
        hidden_layer_output = sigmoid(hidden_layer_input)
        output_layer_input = np.dot(hidden_layer_output, weights_hidden_output) + bias_output
        output_layer_output = sigmoid(output_layer_input)
        return output_layer_output
    

class GeneticAlgorithm():
    
    def __init__(self):    
        # Define the environment and game parameters
        self.num_inputs = 16
        self.num_actions = 4
        self.population_size = 100
        self.num_generations = 50
        self.max_game_steps = 10

        # Create a population of bots (neural networks)
        w_input_hidden, bias_hidden, w_hidden_output, bias_output = create_neural_network(self.num_inputs, 16, self.num_actions)
        
        self.population = [GeneticBot(w_input_hidden, bias_hidden, w_hidden_output, bias_output) for _ in range(self.population_size)]

    # Define a function to evaluate a bot's performance
    def evaluate_bot(self, bot):
        game = Game()
        game.initialize_game()
        while not game.is_game_over():
            next_move = bot.get_next_move(game)
            game.step(next_move)
        return game.get_score()

    def train(self):
        # Main evolution loop using numpy
        for gen in range(self.num_generations):
            # Evaluate each bot in the population
            fitness_scores = [self.evaluate_bot(bot) for bot in self.population]

            # Select top-performing bots based on fitness scores
            num_selected = self.population_size // 2
            selected_indices = np.argsort(fitness_scores)[-num_selected:]

            # Create a new population by copying and mutating the selected bots
            new_population = [population[i] for i in selected_indices]
            print("gen")
            for _ in range(num_selected, self.population_size):
                print("bot")
                # Randomly select two parents
                parent1, parent2 = random.choices(population=population, k=2)

                # Perform crossover operation
                child = crossover(parent1.get_neural_network(), parent2.get_neural_network())

                # Perform mutation operation
                child = mutate(child, mutation_rate=0.1)

                # Append the child bot to the new population
                new_population.append(GeneticBot(child))

            # Update the population
            population = new_population

            # Print the best fitness in this generation
            best_fitness = max(fitness_scores)
            print(f"Generation {gen + 1}: Best Fitness = {best_fitness}")


# Define a simple feedforward neural network
def create_neural_network(input_size, hidden_size, output_size):
    # Initialize weights and biases randomly
    weights_input_hidden = np.random.randn(input_size, hidden_size)
    bias_hidden = np.zeros((1, hidden_size))
    weights_hidden_output = np.random.randn(hidden_size, output_size)
    bias_output = np.zeros((1, output_size))

    return weights_input_hidden, bias_hidden, weights_hidden_output, bias_output

# Crossover operation: One-point crossover
def crossover(parent1, parent2):
    # Randomly select a crossover point
    crossover_point = random.randint(1, len(parent1) - 1)

    # Create a child bot by combining the genes of parents
    child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))

    return child

# Mutation operation: Random mutation with probability mutation_rate
def mutate(bot, mutation_rate):
    for i in range(len(bot)):
        if random.random() < mutation_rate:
            bot[i] += np.random.randn() * 0.1  # Adding random noise as mutation

    return bot

# Sigmoid activation function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Softmax function
def softmax(x):
    exp_x = np.exp(x - np.max(x))  # Subtracting the max value for numerical stability
    return exp_x / exp_x.sum(axis=0, keepdims=True)