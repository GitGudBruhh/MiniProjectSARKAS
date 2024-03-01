import copy
import itertools
import random
from GameData import GameData

class GameHelper:

    def generate_random_code(self, NUM_COLORS: int, CODE_LENGTH: int):
        return [random.randint(1, NUM_COLORS) for _ in range(CODE_LENGTH)]

    # Calculate fitness based on the difference from the actual game feedback
    def calculate_fitness(self, args):
        code, secret_code, CODE_LENGTH, NUM_COLORS = args
        black_pegs = sum(1 for i in range(CODE_LENGTH) if code[i] == secret_code[i])
        white_pegs = sum(min(code.count(j), secret_code.count(j)) for j in range(1, NUM_COLORS + 1)) - black_pegs
        return black_pegs * 2 + white_pegs

    def select_parents(self, population_with_fitness):
        weighted_choices = [(individual, fitness) for individual, fitness in population_with_fitness]
        parents = random.choices(weighted_choices, k=len(weighted_choices)//2)
        return parents

    def crossover(self, parent1, parent2,CODE_LENGTH):
        point = random.randint(1, CODE_LENGTH - 1)
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
    
    def mutate(self,code, MUTATION_RATE, CODE_LENGTH, NUM_COLORS):
        if random.random() < MUTATION_RATE:
            mutation_point = random.randint(0, CODE_LENGTH - 1)
            code[mutation_point] = random.randint(1, NUM_COLORS)
        return code