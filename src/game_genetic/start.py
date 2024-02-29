import random

# Constants for the game
CODE_LENGTH = 6  # Length of the secret code
NUM_COLORS = 8   # Number of different colors
POPULATION_SIZE = 100  # Size of the population
NUM_GENERATIONS = 500   # Maximum number of generations to evolve
MUTATION_RATE = 0.1    # Probability of mutation

# Generate a random secret code
def generate_random_code():
    return [random.randint(1, NUM_COLORS) for _ in range(CODE_LENGTH)]

# Calculate fitness based on the difference from the actual game feedback
def calculate_fitness(code, secret_code):
    black_pegs = sum(1 for i in range(CODE_LENGTH) if code[i] == secret_code[i])
    white_pegs = sum(min(code.count(j), secret_code.count(j)) for j in range(1, NUM_COLORS + 1)) - black_pegs
    # Fitness is the total number of pegs correctly matched; higher is better
    return black_pegs * 2 + white_pegs

# Select parents based on their fitness; higher fitness has a better chance of being selected
def select_parents(population_with_fitness):
    weighted_choices = [(individual, fitness) for individual, fitness in population_with_fitness]
    parents = random.choices(weighted_choices, k=len(weighted_choices)//2)
    return parents

# Crossover between two parents to produce two offspring
def crossover(parent1, parent2):
    point = random.randint(1, CODE_LENGTH - 1)
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

# Mutate an individual code by randomly changing one of its elements
def mutate(code):
    if random.random() < MUTATION_RATE:
        mutation_point = random.randint(0, CODE_LENGTH - 1)
        code[mutation_point] = random.randint(1, NUM_COLORS)
    return code

# Main genetic algorithm for solving Mastermind
def genetic_algorithm(secret_code):
    population = [generate_random_code() for _ in range(POPULATION_SIZE)]
    for generation in range(NUM_GENERATIONS):
        population_with_fitness = [(individual, calculate_fitness(individual, secret_code)) for individual in population]

        if any(fitness == CODE_LENGTH * 2 for _, fitness in population_with_fitness):  # Perfect score
            solution = [individual for individual, fitness in population_with_fitness if fitness == CODE_LENGTH * 2][0]
            print(f"Solution found in generation {generation}: {solution}")
            return solution

        parents = select_parents(population_with_fitness)
        population = []
        while len(population) < POPULATION_SIZE:
            parent1, parent2 = random.sample(parents, 2)
            offspring1, offspring2 = crossover(parent1[0], parent2[0])
            population.append(mutate(offspring1))
            if len(population) < POPULATION_SIZE:
                population.append(mutate(offspring2))
    print("Solution not found within the generation limit.")
    return None

# Example
secret_code = generate_random_code()
print(f"Secret Code: {secret_code}")
solution = genetic_algorithm(secret_code)
if solution:
    print(f"Found Solution: {solution}")
else:
    print("Did not find a solution.")