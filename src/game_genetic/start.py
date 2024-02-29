import random
from GameData import GameData
from GameHelper import GameHelper

# Constants for the game
# CODE_LENGTH = 6  # Length of the secret code
# NUM_COLORS = 8   # Number of different colors
# POPULATION_SIZE = 100  # Size of the population
# NUM_GENERATIONS = 500   # Maximum number of generations to evolve
# MUTATION_RATE = 0.1    # Probability of mutation

gameHelper=GameHelper()

NUM_COLORS = int(input("Enter number of colours: "))
CODE_LENGTH = int(input("Enter number of columns: "))
POPULATION_SIZE=int(input("Enter size of population: "))
NUM_GENERATIONS=int(input("Enter number of generations: "))
MUTATION_RATE=float(input("Enter mutation rate: "))
secret_code=gameHelper.generate_random_code(NUM_COLORS,CODE_LENGTH)
newGameData = GameData(NUM_COLORS, POPULATION_SIZE, CODE_LENGTH, secret_code, NUM_GENERATIONS, MUTATION_RATE)
#Ig we dont need to add game state

# Main genetic algorithm for solving Mastermind
def genetic_algorithm(secret_code):
    population = [gameHelper.generate_random_code(NUM_COLORS,CODE_LENGTH) for _ in range(POPULATION_SIZE)]
    for generation in range(NUM_GENERATIONS):
        population_with_fitness = [(individual, gameHelper.calculate_fitness(individual, secret_code,CODE_LENGTH,NUM_COLORS)) for individual in population]

        if any(fitness == CODE_LENGTH * 2 for _, fitness in population_with_fitness):  # Perfect score
            solution = [individual for individual, fitness in population_with_fitness if fitness == CODE_LENGTH * 2][0]
            print(f"Solution found in generation {generation}: {solution}")
            return solution

        parents = gameHelper.select_parents(population_with_fitness)
        population = []
        while len(population) < POPULATION_SIZE:
            parent1, parent2 = random.sample(parents, 2)
            offspring1, offspring2 = gameHelper.crossover(parent1[0], parent2[0],CODE_LENGTH)
            population.append(gameHelper.mutate(offspring1,MUTATION_RATE,CODE_LENGTH,NUM_COLORS))
            if len(population) < POPULATION_SIZE:
                population.append(gameHelper.mutate(offspring2,MUTATION_RATE,CODE_LENGTH,NUM_COLORS))
    print("Solution not found within the generation limit.")
    return None

# Example
# secret_code = generate_random_code()
print(f"Secret Code: {secret_code}")
solution = genetic_algorithm(secret_code)
if solution:
    print(f"Found Solution: {solution}")
else:
    print("Did not find a solution.")