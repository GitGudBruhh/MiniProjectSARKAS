import random

CODE_LENGTH = 4
POPULATION_SIZE = 50
MAX_GENERATIONS = 500
MUTATION_RATE = 0.1

def generate_secret_code():
    return [random.randint(1, 6) for _ in range(CODE_LENGTH)]

def calculate_fitness(guess, secret_code):
    # Calculate fitness based on the number of correct positions and colors
    correct_positions = sum([1 for i in range(CODE_LENGTH) if guess[i] == secret_code[i]])
    correct_colors = sum([1 for color in set(guess) if guess.count(color) <= secret_code.count(color)])
    return correct_positions + correct_colors

def generate_population():
    return [[random.randint(1, 6) for _ in range(CODE_LENGTH)] for _ in range(POPULATION_SIZE)]

def selection(population, secret_code):
    return sorted(population, key=lambda x: calculate_fitness(x, secret_code), reverse=True)[:2]

def crossover(parent1, parent2):
    crossover_point = random.randint(1, CODE_LENGTH - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def mutation(child):
    for i in range(CODE_LENGTH):
        if random.random() < MUTATION_RATE:
            child[i] = random.randint(1, 6)
    return child

def genetic_algorithm(secret_code):
    population = generate_population()
    generation = 0

    while generation < MAX_GENERATIONS:
        parents = selection(population, secret_code)
        offspring = [crossover(parents[0], parents[1]) for _ in range(POPULATION_SIZE)]
        population = [mutation(child) for child in offspring]

        best_guess = max(population, key=lambda x: calculate_fitness(x, secret_code))
        if calculate_fitness(best_guess, secret_code) == CODE_LENGTH:
            return best_guess

        generation += 1

    return None

if __name__ == "__main__":
    secret_code = generate_secret_code()
    print("Secret Code:", secret_code)

    best_guess = genetic_algorithm(secret_code)
    if best_guess:
        print("Best Guess Found:", best_guess)
    else:
        print("Algorithm did not find the secret code within the maximum genrations")

#dynamic population
#elitism , cross over and mutation
#diversification
#local search 