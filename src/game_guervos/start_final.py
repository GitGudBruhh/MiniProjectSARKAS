import random
from GameData import GameData
from GameHelper import GameHelper
from concurrent.futures import ProcessPoolExecutor
import copy

# Constants for the game
# CODE_LENGTH = 6  # Length of the secret code
# NUM_COLORS = 8   # Number of different colors
# POPULATION_SIZE = 100  # Size of the population
# NUM_GENERATIONS = 500   # Maximum number of generations to evolve
# MUTATION_RATE = 0.1    # Probability of mutation

# gameHelper=GameHelper()
#
# NUM_COLORS = int(input("Enter number of colours: "))
# CODE_LENGTH = int(input("Enter number of columns: "))
# POPULATION_SIZE=int(input("Enter size of population: "))
# NUM_GENERATIONS=int(input("Enter number of generations: "))
# MUTATION_RATE=float(input("Enter mutation rate: "))
# secret_code=gameHelper.generate_random_code(NUM_COLORS,CODE_LENGTH)
# newGameData = GameData(NUM_COLORS, POPULATION_SIZE, CODE_LENGTH, secret_code, NUM_GENERATIONS, MUTATION_RATE)
# MAX_WORKERS = 4  # Number of processes to use for parallel execution

#Ig we dont need to add game state

# Main genetic algorithm for solving Mastermind
# def genetic_algorithm(secret_code):
#     population = [gameHelper.generate_random_code(NUM_COLORS,CODE_LENGTH) for _ in range(POPULATION_SIZE)]
#     for generation in range(NUM_GENERATIONS):
#         population_with_fitness = [(individual, gameHelper.calculate_fitness(individual, secret_code,CODE_LENGTH,NUM_COLORS)) for individual in population]
#
#         if any(fitness == CODE_LENGTH * 2 for _, fitness in population_with_fitness):  # Perfect score
#             solution = [individual for individual, fitness in population_with_fitness if fitness == CODE_LENGTH * 2][0]
#             print(f"Solution found in generation {generation}: {solution}")
#             return solution
#
#         parents = gameHelper.select_parents(population_with_fitness)
#         population = []
#         while len(population) < POPULATION_SIZE:
#             parent1, parent2 = random.sample(parents, 2)
#             offspring1, offspring2 = gameHelper.crossover(parent1[0], parent2[0],CODE_LENGTH)
#             population.append(gameHelper.mutate(offspring1,MUTATION_RATE,CODE_LENGTH,NUM_COLORS))
#             if len(population) < POPULATION_SIZE:
#                 population.append(gameHelper.mutate(offspring2,MUTATION_RATE,CODE_LENGTH,NUM_COLORS))
#     print("Solution not found within the generation limit.")
#     return None

# Main genetic algorithm with parallel fitness calculation
def genetic_algorithm(secret_code, numColors, codeLength, populationSize, numGenerations, mutationRate):
    
        #Generating random population
        population = [gameHelper.generate_random_code(numColors,codeLength) for _ in range(populationSize)]

        #Empty Guess List
        Guess_List = []
        
        count = 0
        
        '''
        For choosing custom initial guess

        while(True): 
            playerGuessStr = input("Enter first guess: ")
            playerFirstGuess =[int(color) for color in playerGuessStr.split(" ")]
            if gameHelper.isValidGuess(newGameData, playerFirstGuess) == True:
                Guess_List.append(playerFirstGuess)
                break
        '''

        # Generating Random initaial guess
        Guess_List = [gameHelper.generate_random_code(numColors,codeLength)]
        print("Initial Guess:",Guess_List[0])
        
        #Starting at generation 0
        for generation in range(numGenerations): 
            #Hypermutation (Reset population if consitent combination not found in 15 successive generations)
            if count == 15:
                population = [gameHelper.generate_random_code(numColors,codeLength) for _ in range(populationSize)]
                count = 0
            
            t=[] # list to store fitnesses for each element in population
            
            #Calculating fitness for each element in population
            for individual in population:
                total_dist=0
                for c_i in Guess_List:
                    args = (individual, c_i,codeLength,numColors) 
                    h = gameHelper.hint(args)
                    args_g = (c_i, secret_code,codeLength,numColors)
                    h_i = gameHelper.hint(args_g)
                    total_dist +=  gameHelper.distance(h,h_i)
                t.append(total_dist)

            #List containing (fitness,element)        
            population_with_fitness = list(zip(map(gameHelper.calculate_fitness, t), population))

            #Sorting from least to greatest fitness
            population_with_fitness.sort()
            #print(population_with_fitness)
            #print('\n')
            
            #Checking whether there is an element with fitness 0 (a consistent element) and chossing it as a guess
            if population_with_fitness[-1][0] == 0 and population_with_fitness[-1][1] not in Guess_List :
                count = 0
                Guess_List.append(copy.deepcopy(population_with_fitness[-1][1]))

            else:
                count+=1
            

            print(Guess_List) #Displaying guesses in each generation

            #Checking if secret code obtained (ie last elemnt of guess list is secret code)
            if gameHelper.hint((Guess_List[-1],secret_code,codeLength,numColors))[0] == codeLength:
                print(f"Solution found in generation {generation}: {Guess_List[-1]}")
                print("Number of Guesses:",len(Guess_List))
                return Guess_List[-1]

            
            half = populationSize//2 
            
            # Storing the half of the original population with lower fitness in the new population
            population = [code for _ , code in copy.deepcopy(population_with_fitness)[half:]]
            # 20% of the (new) population to be transposed
            transposition_size = int(0.2* len(population)) #1
            # 40% of the (new) population to be crossed-over
            crossover_size = int(0.4* len(population)) #2 
            # 40% of the (new) population to be circular mutated
            c_mutate_size = len(population) - transposition_size - crossover_size #2
            
            #Set to be transposed
            transposition_set = random.sample(copy.deepcopy(population), transposition_size)
            #Set to be crossed-over
            co_set = random.sample(copy.deepcopy(population), crossover_size)
            #Set to be circular mutated
            cm_set = random.sample(copy.deepcopy(population), c_mutate_size)
            
            #Applying transposition on elements in transposition set at adding them to population 
            i = 0 
            while i < transposition_size:
                population.append(gameHelper.transpose(transposition_set[i]))
                i+=1
            
            #Applying crossover on elements in crossover set at adding them to population
            i = 0
            while i < (crossover_size):
                parent1, parent2 = random.sample(co_set, 2)
                offspring1, offspring2 = gameHelper.crossover(parent1, parent2,codeLength)
                population.append(offspring1)
                i+=1
                if i < crossover_size:
                    population.append(offspring2)
                i+=1
            
            #Applying circular mutation on elements in circular mutation set at adding them to population
            i = 0
            while i  < (c_mutate_size):
                population.append(gameHelper.circular_mutate(cm_set[i]))
                i+=1
            

            #Case when generation is insufficient to obtain secret code restart    
           

        #return None


if __name__ == "__main__":
    NUM_COLORS = int(input("Enter number of colours: "))
    CODE_LENGTH = int(input("Enter number of columns: "))
    POPULATION_SIZE = int(input("Enter size of population: "))
    NUM_GENERATIONS = int(input("Enter number of generations: "))
    #MUTATION_RATE = float(input("Enter mutation rate: "))
    gameHelper=GameHelper()
    secret_code=gameHelper.generate_random_code(NUM_COLORS,CODE_LENGTH)
    newGameData = GameData(NUM_COLORS, POPULATION_SIZE, CODE_LENGTH, secret_code, NUM_GENERATIONS, 0)
    print(f"Secret Code: {secret_code}")
    solution = genetic_algorithm(secret_code, NUM_COLORS, CODE_LENGTH, POPULATION_SIZE, NUM_GENERATIONS, 0)
    if solution:
        print(f"Found Solution: {solution}")
    else:
        print("Did not find a solution.")
