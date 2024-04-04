import random
from GameData import GameData
from GameHelper import GameHelper
import copy

count = 0


def genetic_algorithm(secret_code, numColors, codeLength, populationSize, numGenerations, mutationRate, permutationRate,inversionRate):
    i = 0
    previous_set=set()
    gameHelper = GameHelper()
    Intial_Guess = gameHelper.generate_random_code(numColors, codeLength)
    args = (Intial_Guess, secret_code, codeLength, numColors)
    pegs = gameHelper.hint(args)
    print(f"Initial Guess:{Intial_Guess}")
    Guess_List = [[Intial_Guess, gameHelper.hint((Intial_Guess, secret_code, codeLength, numColors))]]
    Eligible_set = set()
    population = [gameHelper.generate_random_code(numColors, codeLength) for _ in range(populationSize)]
    while (pegs[0] != codeLength):
        if i>20:
            break
        i += 1
        h = 1
        C =0
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
                if child1 and child2 not in new_population:
                    new_population.extend([child1, child2])
            population = random.sample(new_population, populationSize)

            fitness_list = []
            for individual in population:
                fitness_list.append(gameHelper.calculate_fitness(individual, Guess_List, 1, 2, codeLength))

            population_with_fitness = list(zip(fitness_list, population))
            population_with_fitness.sort(key=lambda x: x[0])
            for k in range(len(population_with_fitness)):
                if len(Eligible_set) >= populationSize:
                    break
                if population_with_fitness[k][0] == 2 * codeLength * (len(Guess_List) - 1) and tuple(
                        population_with_fitness[k][1]) not in Eligible_set:
                    Eligible_set.add(copy.deepcopy(tuple(population_with_fitness[k][1])))
            
            if (len(Eligible_set)==0):
                C+=1
            else:
                C=0
            if(C>500):
                C=0
                population = [gameHelper.generate_random_code(numColors, codeLength) for _ in range(populationSize)]
            h += 1

        if len(Eligible_set)<=3:
            Eligible_set = set(list(previous_set) +list(Eligible_set))
        previous_set = Eligible_set
        print("PS:",previous_set)
        Random_Guess = random.choice(list(Eligible_set))

        if ([Random_Guess, tuple(gameHelper.hint((Random_Guess, secret_code, codeLength, numColors)))] not in Guess_List):
            Guess_List.append(
                copy.deepcopy([Random_Guess, tuple(gameHelper.hint((Random_Guess, secret_code, codeLength, numColors)))]))
        
        print("GL:", Guess_List)
        a = (Random_Guess, secret_code, codeLength, numColors)
        pegs = gameHelper.hint(a)
        Eligible_set = set()

    if pegs[0]==codeLength:
        print(f"Solution found: {Guess_List[-1]}")
        print("Number of Guesses:", len(Guess_List))
    print("Did not find solution")
    return Guess_List[-1]


if __name__ == "__main__":
    NUM_COLORS = int(input("Enter number of colours: "))
    CODE_LENGTH = int(input("Enter number of columns: "))
    POPULATION_SIZE = int(input("Enter size of population: "))
    NUM_GENERATIONS = int(input("Enter number of generations: "))
    gameHelper = GameHelper()
    secret_code = gameHelper.generate_random_code(NUM_COLORS, CODE_LENGTH)
    newGameData = GameData(NUM_COLORS, POPULATION_SIZE, CODE_LENGTH, secret_code, NUM_GENERATIONS, 0.1, 0.05, 0.05)
    print(f"Secret Code: {secret_code}")
    solution = genetic_algorithm(secret_code, NUM_COLORS, CODE_LENGTH, POPULATION_SIZE, NUM_GENERATIONS, 0.1, 0.05,0.05)
    
