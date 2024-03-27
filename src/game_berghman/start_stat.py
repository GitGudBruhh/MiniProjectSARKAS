import random
from GameData import GameData
from GameHelper import GameHelper
# from concurrent.futures import ProcessPoolExecutor
import copy

count = 0



# Main genetic algorithm with parallel fitness calculation
def genetic_algorithm(secret_code, numColors, codeLength, populationSize, numGenerations, mutationRate, permutationRate,inversionRate):
    i = 0
    gameHelper = GameHelper()
    Intial_Guess = gameHelper.generate_random_code(numColors, codeLength)
    args = (Intial_Guess, secret_code, codeLength, numColors)
    pegs = gameHelper.hint(args)
    print(f"Initial Guess:{Intial_Guess}")
    Guess_List = [[Intial_Guess, gameHelper.hint((Intial_Guess, secret_code, codeLength, numColors))]]
    while (pegs[0] != codeLength):
        i += 1
        h = 1
        Eligible_set = set()
        # Eligible_set = generating_eligible_set(secret_code, numColors, codeLength, populationSize, numGenerations, mutationRate, permutationRate,inversionRate,Guess_List)
        while len(Eligible_set)==0:
            print(1)
            Eligible_set = generating_eligible_set(secret_code, numColors, codeLength, populationSize, numGenerations, mutationRate, permutationRate,inversionRate,Guess_List)
        Random_Guess = random.choice(list(Eligible_set))

        Guess_List.append(
            copy.deepcopy([Random_Guess, tuple(gameHelper.hint((Random_Guess, secret_code, codeLength, numColors)))]))
        print("GL:", Guess_List)
        a = (Random_Guess, secret_code, codeLength, numColors)
        pegs = gameHelper.hint(a)

    print(f"Solution found: {Guess_List[-1]}")
    print("Number of Guesses:", len(Guess_List))
    return Guess_List[-1]

def generating_eligible_set(secret_code, numColors, codeLength, populationSize, numGenerations, mutationRate, permutationRate,inversionRate,Guess_List):
    population = [gameHelper.generate_random_code(numColors, codeLength) for _ in range(populationSize)]
    eligible_set =set()
    h=0
    while h <= numGenerations:
        new_population = []
        for _ in range(populationSize):
            parent1, parent2 = random.sample(population, 2)
            if random.random() < 0.5:
                child1, child2 = gameHelper.one_point_crossover(parent1, parent2, codeLength)
            else:
                child1, child2 = gameHelper.two_point_crossover(parent1, parent2, codeLength)
            child1 = gameHelper.mutate(child1, mutationRate, codeLength, numColors)
            child2 = gameHelper.mutate(child2, mutationRate, codeLength, numColors)
            child1 = gameHelper.permute(child1, permutationRate, codeLength, numColors)
            child2 = gameHelper.permute(child2, permutationRate, codeLength, numColors)
            child1 = gameHelper.invert(child1, inversionRate, codeLength, numColors)
            child2 = gameHelper.invert(child2, inversionRate, codeLength, numColors)
            new_population.extend([child1, child2])
        population = random.sample(new_population, populationSize)

        fitness_list = []
        for individual in population:
            fitness_list.append(gameHelper.calculate_fitness(individual, Guess_List, 1, 2, codeLength))

        # List containing (fitness,element)
        population_with_fitness = list(zip(fitness_list, population))
        population_with_fitness.sort(key=lambda x: x[0])
        # print("Pop with fit:", population_with_fitness)
        # print(2*codeLength*(len(Guess_List)-1))
        for k in range(len(population_with_fitness)):
            if len(eligible_set) >= populationSize:
                break
            if population_with_fitness[k][0] == 2 * codeLength * (len(Guess_List) - 1) and tuple(
                    population_with_fitness[k][1]) not in eligible_set:
                eligible_set.add(copy.deepcopy(tuple(population_with_fitness[k][1])))

        h += 1
    return eligible_set

if __name__ == "__main__":
    NUM_COLORS = int(input("Enter number of colours: "))
    CODE_LENGTH = int(input("Enter number of columns: "))
    POPULATION_SIZE = int(input("Enter size of population: "))
    NUM_GENERATIONS = int(input("Enter number of generations: "))
    # MUTATION_RATE = float(input("Enter mutation rate: "))
    # PERMUTATION_RATE = float(input("Enter mutation rate: "))
    # INVERSION_RATE = float(input("Enter mutation rate: "))
    gameHelper = GameHelper()
    secret_code = gameHelper.generate_random_code(NUM_COLORS, CODE_LENGTH)
    newGameData = GameData(NUM_COLORS, POPULATION_SIZE, CODE_LENGTH, secret_code, NUM_GENERATIONS, 0.05, 0.05, 0.03)
    print(f"Secret Code: {secret_code}")
    solution = genetic_algorithm(secret_code, NUM_COLORS, CODE_LENGTH, POPULATION_SIZE, NUM_GENERATIONS, 0.05, 0.05,0.03)
    if solution:
        print(f"Found Solution: {solution}")
    else:
        print("Did not find a solution.")
