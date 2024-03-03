import random
from GameData import GameData
from GameHelper import GameHelper
from concurrent.futures import ProcessPoolExecutor

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
def genetic_algorithm(secret_code, numColors, codeLength, populationSize, numGenerations, mutationRate, maxWorkers):
    population = [gameHelper.generate_random_code(numColors,codeLength) for _ in range(populationSize)]
    Guess_List = []
    

    with ProcessPoolExecutor(max_workers=maxWorkers) as executor:
        
        '''
        while(True): 
            playerGuessStr = input("Enter first guess: ")
            playerFirstGuess =[int(color) for color in playerGuessStr.split(" ")]
            if gameHelper.isValidGuess(newGameData, playerFirstGuess) == True:
                Guess_List.append(playerFirstGuess)
                break
        '''        
        
        Guess_List = [gameHelper.generate_random_code(numColors,codeLength)]
        print("Initial Guess:",Guess_List[0])

        for generation in range(numGenerations):
            # Parallel calculation of fitness
            #print(Guess_List)
            t=[]
           
            for individual in population:
                total_dist=0
                for c_i in Guess_List:
                    args = (individual, c_i,codeLength,numColors) 
                    h = gameHelper.hint(args)
                    args_g = (c_i, secret_code,codeLength,numColors)
                    h_i = gameHelper.hint(args_g)
                    total_dist +=  gameHelper.distance(h,h_i)
                
                t.append((total_dist))
                    
            population_with_fitness = list(zip(executor.map(gameHelper.calculate_fitness, t), population))

            population_with_fitness.sort()

            
            
            if population_with_fitness[-1][0] == 0 and population_with_fitness[-1][1] not in Guess_List :
                Guess_List.append(population_with_fitness[-1][1])


            print(Guess_List)
            if gameHelper.hint((Guess_List[-1],secret_code,codeLength,numColors))[0] == codeLength:
               
                print(f"Solution found in generation {generation}: {Guess_List[-1]}")
                return Guess_List[-1]


           

            
            half = populationSize//2
            

            
            population = [code for _ , code in population_with_fitness[half:]]
            transposition_size = int(0.2* len(population)) #1
            crossover_size = int(0.4* len(population)) #2 
            c_mutate_size = len(population) - transposition_size - crossover_size #2
            
            transposition_set = random.sample(population, transposition_size)
            co_set = random.sample(population, crossover_size)
            cm_set = random.sample(population, c_mutate_size)
            #print("before:",len(population))
            i = 0 
            while i < transposition_size:
                population.append(gameHelper.transpose(transposition_set[i]))
                #print(c)
                i+=1
            #print(len(population))
            i = 0
            while i < (crossover_size):
                parent1, parent2 = random.sample(co_set, 2)
                offspring1, offspring2 = gameHelper.crossover(parent1, parent2,codeLength)
                population.append(offspring1)
                i+=1
                if i < crossover_size:
                    population.append(offspring2)
                i+=1
            
            #print(len(population))
            i = 0
            while i  < (c_mutate_size):
                population.append(gameHelper.circular_mutate(cm_set[i]))
                i+=1

            #print("\n")
            #print((population))
            #print("\n")

    print("Solution not found within the generation limit.")
    return None

# Example
# secret_code = generate_random_code()
if __name__ == "__main__":
    NUM_COLORS = int(input("Enter number of colours: "))
    CODE_LENGTH = int(input("Enter number of columns: "))
    POPULATION_SIZE = int(input("Enter size of population: "))
    NUM_GENERATIONS = int(input("Enter number of generations: "))
    #MUTATION_RATE = float(input("Enter mutation rate: "))
    gameHelper=GameHelper()
    secret_code=gameHelper.generate_random_code(NUM_COLORS,CODE_LENGTH)
    newGameData = GameData(NUM_COLORS, POPULATION_SIZE, CODE_LENGTH, secret_code, NUM_GENERATIONS, 0)
    MAX_WORKERS = 4  # Number of processes to use for parallel execution
    print(f"Secret Code: {secret_code}")
    solution = genetic_algorithm(secret_code, NUM_COLORS, CODE_LENGTH, POPULATION_SIZE, NUM_GENERATIONS, 0, MAX_WORKERS)
    if solution:
        print(f"Found Solution: {solution}")
    else:
        print("Did not find a solution.")
