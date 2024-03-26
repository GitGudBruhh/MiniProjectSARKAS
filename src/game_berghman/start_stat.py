import random
from GameData import GameData
from GameHelper import GameHelper
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
        # Generating random population
        population = [gameHelper.generate_random_code(numColors, codeLength) for _ in range(populationSize)]

        # Generating Random initaial guess
        # Guess_List = [gameHelper.generate_random_code(numColors,codeLength)]
        # print(len(Guess_List))

        while len(Eligible_set) < populationSize and  h <= numGenerations:
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

            # t=[] # list to store fitnesses for each element in population
            #
            # #Calculating fitness for each element in population
            # for individual in population:
            #     total_dist=0
            #     for c_i in Guess_List:
            #         args = (individual, c_i,codeLength,numColors)
            #         h1 = gameHelper.hint(args)
            #         args_g = (c_i, secret_code,codeLength,numColors)
            #         h_i = gameHelper.hint(args_g)
            #         total_dist +=  gameHelper.distance(h1,h_i,len(Guess_List),codeLength)
            #     t.append(total_dist)

            fitness_list = []
            for individual in population:
                fitness_list.append(gameHelper.calculate_fitness(individual, Guess_List, 1, 2, codeLength))

            # List containing (fitness,element)
            population_with_fitness = list(zip(fitness_list, population))
            population_with_fitness.sort(key=lambda x: x[0])
            # print("Pop with fit:", population_with_fitness)
            # print(2*codeLength*(len(Guess_List)-1))
            for k in range(len(population_with_fitness)):
                if len(Eligible_set) >= populationSize:
                    break
                if population_with_fitness[k][0] == 2 * codeLength * (len(Guess_List) - 1) and tuple(
                        population_with_fitness[k][1]) not in Eligible_set:
                    Eligible_set.add(copy.deepcopy(tuple(population_with_fitness[k][1])))

            h += 1
        # print("ES:", Eligible_set)
        # Exception handling
        try:
            Random_Guess = random.choice(list(Eligible_set))
        except:
            global count
            count+=1
            print(count)
            if count==100:
                print("Arrrrgggghhh!!!! I give up!")
                exit(100)

        Guess_List.append(
            copy.deepcopy([Random_Guess, tuple(gameHelper.hint((Random_Guess, secret_code, codeLength, numColors)))]))
        print("GL:", Guess_List)
        a = (Random_Guess, secret_code, codeLength, numColors)
        pegs = gameHelper.hint(a)

    print(f"Solution found: {Guess_List[-1]}")
    print("Number of Guesses:", len(Guess_List))
    return Guess_List[-1]


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
    newGameData = GameData(NUM_COLORS, POPULATION_SIZE, CODE_LENGTH, secret_code, NUM_GENERATIONS, 0.05, 0.05, 0.04)
    print(f"Secret Code: {secret_code}")
    solution = genetic_algorithm(secret_code, NUM_COLORS, CODE_LENGTH, POPULATION_SIZE, NUM_GENERATIONS, 0.05, 0.05,0.04)
    if solution:
        print(f"Found Solution: {solution}")
    else:
        print("Did not find a solution.")
