import random
from GameData import GameData
from GameHelper import GameHelper
# from concurrent.futures import ProcessPoolExecutor
import copy

#population size=150

# import random

# CODE_LENGTH = 4
# POPULATION_SIZE = 50
# MAX_GENERATIONS = 500
# MUTATION_RATE = 0.1

# def generate_secret_code():
#     return [random.randint(1, 6) for _ in range(CODE_LENGTH)]

# def calculate_fitness(guess, secret_code):
#     # Calculate fitness based on the number of correct positions and colors
#     correct_positions = sum([1 for i in range(CODE_LENGTH) if guess[i] == secret_code[i]])
#     correct_colors = sum([1 for color in set(guess) if guess.count(color) <= secret_code.count(color)])
#     return correct_positions + correct_colors

# def generate_population():
#     return [[random.randint(1, 6) for _ in range(CODE_LENGTH)] for _ in range(POPULATION_SIZE)]

# def selection(population, secret_code):
#     return sorted(population, key=lambda x: calculate_fitness(x, secret_code), reverse=True)[:2]

# def crossover(parent1, parent2):
#     crossover_point = random.randint(1, CODE_LENGTH - 1)
#     child = parent1[:crossover_point] + parent2[crossover_point:]
#     return child

# def mutation(child):
#     for i in range(CODE_LENGTH):
#         if random.random() < MUTATION_RATE:
#             child[i] = random.randint(1, 6)
#     return child

# def genetic_algorithm(secret_code):
#     population = generate_population()
#     generation = 0

#     while generation < MAX_GENERATIONS:
#         parents = selection(population, secret_code)
#         offspring = [crossover(parents[0], parents[1]) for _ in range(POPULATION_SIZE)]
#         population = [mutation(child) for child in offspring]

#         best_guess = max(population, key=lambda x: calculate_fitness(x, secret_code))
#         if calculate_fitness(best_guess, secret_code) == CODE_LENGTH:
#             return best_guess

#         generation += 1

#     return None

# if __name__ == "__main__":
#     secret_code = generate_secret_code()
#     print("Secret Code:", secret_code)

#     best_guess = genetic_algorithm(secret_code)
#     if best_guess:
#         print("Best Guess Found:", best_guess)
#     else:
#         print("Algorithm did not find the secret code within the maximum genrations")


# Main genetic algorithm with parallel fitness calculation
def genetic_algorithm(secret_code, numColors, codeLength, populationSize, numGenerations, mutationRate, permutationRate, inversionRate):
    i=0
    gameHelper = GameHelper()
    Intial_Guess=[1,1,2,3]
    args=(Intial_Guess,secret_code,codeLength,numColors)
    pegs=gameHelper.hint(args)
    print("Initial Guess:",[1,1,2,3])
    Guess_List = [[1,1,2,3]]
    while(pegs[0]!=codeLength):
        i+=1 
        h=1
        Eligible_set=[]
        #Generating random population
        population = [gameHelper.generate_random_code(numColors,codeLength) for _ in range(populationSize)]

        # Generating Random initaial guess
        # Guess_List = [gameHelper.generate_random_code(numColors,codeLength)]
        # print(len(Guess_List))
        
        
        while h <= numGenerations:
            new_population=[]
            for _ in range(populationSize):
                parent1, parent2 = random.sample(population, 2)
                if random.random() < 0.5:
                    child1, child2 = gameHelper.one_point_crossover(parent1, parent2,codeLength)
                else:
                    child1, child2 = gameHelper.two_point_crossover(parent1, parent2,codeLength)
                child1 = gameHelper.mutate(child1, mutationRate,codeLength,numColors)
                child2 = gameHelper.mutate(child2, mutationRate,codeLength,numColors)
                child1 = gameHelper.permute(child1, permutationRate,codeLength,numColors)
                child2 = gameHelper.permute(child2, permutationRate,codeLength,numColors)
                child1 = gameHelper.invert(child1, inversionRate,codeLength,numColors)
                child2 = gameHelper.invert(child2, inversionRate,codeLength,numColors)
                new_population.extend([child1, child2])
            population = random.sample(new_population, populationSize)

            t=[] # list to store fitnesses for each element in population
        
            #Calculating fitness for each element in population
            for individual in population:
                total_dist=0
                for c_i in Guess_List:
                    args = (individual, c_i,codeLength,numColors) 
                    h1 = gameHelper.hint(args)
                    args_g = (c_i, secret_code,codeLength,numColors)
                    h_i = gameHelper.hint(args_g)
                    total_dist +=  gameHelper.distance(h1,h_i,len(Guess_List),codeLength)
                t.append(total_dist)

            #List containing (fitness,element)        
            population_with_fitness = list(zip(map(gameHelper.calculate_fitness, t), population))
            population_with_fitness.sort()
            print("Pop with fit:",population_with_fitness)
            #print(2*codeLength*(len(Guess_List)-1))
            for k in range(len(population_with_fitness)):
                if len(Eligible_set)>=populationSize:
                    break
                if population_with_fitness[k][0] == 2*codeLength*(len(Guess_List)-1) and population_with_fitness[k][1] not in Eligible_set :
                    Eligible_set.append(copy.deepcopy(population_with_fitness[k][1]))
            
            h+=1
        print("ES:",Eligible_set)
        Random_Guess=random.choice(Eligible_set)
        #print(Random_Guess)
        Guess_List.append(copy.deepcopy(Random_Guess))
        print("GL:",Guess_List)
        a=(Random_Guess,secret_code,codeLength,numColors)
        pegs=gameHelper.hint(a)

    print(f"Solution found: {Guess_List[-1]}")
    print("Number of Guesses:",len(Guess_List))
    return Guess_List[-1]
        

if __name__ == "__main__":
    NUM_COLORS = int(input("Enter number of colours: "))
    CODE_LENGTH = int(input("Enter number of columns: "))
    POPULATION_SIZE = int(input("Enter size of population: "))
    NUM_GENERATIONS = int(input("Enter number of generations: "))
    # MUTATION_RATE = float(input("Enter mutation rate: "))
    # PERMUTATION_RATE = float(input("Enter mutation rate: "))
    # INVERSION_RATE = float(input("Enter mutation rate: "))
    gameHelper=GameHelper()
    secret_code=gameHelper.generate_random_code(NUM_COLORS,CODE_LENGTH)
    newGameData = GameData(NUM_COLORS, POPULATION_SIZE, CODE_LENGTH, secret_code, NUM_GENERATIONS, 0.03,0.03,0.02)
    print(f"Secret Code: {secret_code}")
    solution = genetic_algorithm(secret_code, NUM_COLORS, CODE_LENGTH, POPULATION_SIZE, NUM_GENERATIONS, 0.03, 0.03, 0.02)
    if solution:
        print(f"Found Solution: {solution}")
    else:
        print("Did not find a solution.")
