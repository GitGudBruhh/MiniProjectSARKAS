import copy
import itertools
import random
from GameData import GameData

class GameHelper:

    def generate_random_code(self, NUM_COLORS: int, CODE_LENGTH: int):
        return [random.randint(1, NUM_COLORS) for _ in range(CODE_LENGTH)]
    
    
    def isValidGuess(self, gameData: GameData, playerGuess: list[str]):
        if not (len(playerGuess) == gameData.getNoSlots()):
            print("Length of guess not equal to number of slots")
            return False

        colourRange = list(range(1, gameData.getNoColours() + 1))
        for colour in playerGuess:
            if not int(colour) in colourRange:
                print("Guess values out of range")
                return False

        return True

    # Calculate fitness based on the difference from the actual game feedback
    def hint(self,args):
        code, secret_code, CODE_LENGTH, NUM_COLORS = args
        black_pegs = sum(1 for i in range(CODE_LENGTH) if code[i] == secret_code[i])
        white_pegs = sum(min(code.count(j), secret_code.count(j)) for j in range(1, NUM_COLORS + 1)) - black_pegs
        return [black_pegs,white_pegs]

    def distance(self,peg_list1,peg_list2):
        d = abs(peg_list1[0]-peg_list2[0])+abs(peg_list1[1]-peg_list2[1])
        return d

    def calculate_fitness(self,args):
        total_dist = args
        fitness = -total_dist
        return fitness
        
        

    def select_parents(self, population_with_fitness):
        weighted_choices = [(individual, fitness) for fitness, individual in population_with_fitness]
        parents = random.choices(weighted_choices, k=len(weighted_choices)//2)
        return parents

    def crossover(self, parent1, parent2,CODE_LENGTH):
        point = random.randint(1, CODE_LENGTH - 1)
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
    
    def circular_mutate(self,code):
        new_code = []
        new_code.append(code[-1])
        new_code = new_code + code[:-1]
        return new_code
    
    def transpose(self,code):
        new_code = code
        tc_index = random.randint(0, len(code) - 1)
        transposed_color = new_code.pop(tc_index)
        insertion_point = random.randint(0, len(code) - 1)
        new_code.insert(insertion_point, transposed_color)
        return new_code


    def mutate(self,code, MUTATION_RATE, CODE_LENGTH, NUM_COLORS):
        if random.random() < MUTATION_RATE:
            mutation_point = random.randint(0, CODE_LENGTH - 1)
            code[mutation_point] = random.randint(1, NUM_COLORS)
        return code