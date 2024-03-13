import random
import copy
import numpy as np
import matplotlib.pyplot as plt
from GameHelper import GameHelper
from GameData import GameData


def genetic_algorithm(secret_code, numColors, codeLength, populationSize, numGenerations, mutationRate):
            #Generating random population
            population = [gameHelper.generate_random_code(numColors,codeLength) for _ in range(populationSize)]

            count = 0

            #Empty Guess List
            Guess_List = []
            
            '''
            For choosing custom initial guess

            while(True): 
                playerGuessStr = input("Enter first guess: ")
                playerFirstGuess =[int(color) for color in playerGuessStr.split(" ")]
                if gameHelper.isValidGuess(newGameData, playerFirstGuess) == True:
                    Guess_List.append(playerFirstGuess)
                    break
            '''
            comb_eval = []
            
            # Generating Random initaial guess
            Guess_List = [gameHelper.generate_random_code(numColors,codeLength)]
            #Guess_List = [[1,1,2,2]] # [1,1,2,2] 4.59 [1,2,3,4] 4.60
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
                    if (individual not in comb_eval):
                        comb_eval.append(individual)
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

                #print(Guess_List) #Displaying guesses in each generation

                #Checking if secret code obtained (ie last elemnt of guess list is secret code)
                if gameHelper.hint((Guess_List[-1],secret_code,codeLength,numColors))[0] == codeLength:
                    print(f"Solution found in generation {generation}: {Guess_List[-1]}")
                    guess_no = len(Guess_List)
                    print("No. of guesses:",guess_no)
                    comb = len(comb_eval)
                    return guess_no ,comb

                
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
            

        #return None


colors = [7,8,9,10]
Avg_guess=[]
SD_guess =[]
Avg_comb = []
SD_comb = []
for color in colors:
    print("COLOR COUNT",color)
    i=0
    Sum=0
    total_comb = 0
    l = []
    comb_eval_l=[]
    while(i<100):
        print("run",i)
        gameHelper=GameHelper()
        secret_code=gameHelper.generate_random_code(color,7)
        newGameData = GameData(color, 400, 7 , secret_code, 10000, 0)
        print(f"Secret Code: {secret_code}")
        guess_no, comb = genetic_algorithm(secret_code, color, 7, 400, 10000, 0)
        l.append(guess_no)
        comb_eval_l.append(comb)
        Sum+=guess_no
        total_comb+=comb
        print('\n')
        i+=1
    
    Avg_guess.append(Sum/(i+1))
    SD_guess.append((sum([((g-Sum/(i+1))**2)/(i+1) for g in l]))**(0.5))
    Avg_comb.append((total_comb/(i+1)))
    SD_comb.append(((sum([((g-total_comb/(i+1))**2)/(i+1) for g in comb_eval_l])))**(0.5))

plt.plot(colors,Avg_guess)
plt.xlabel("Color Count")
plt.ylabel("Average Guesses (7 slots)")
plt.show()

X=np.array([[color,1] for color in colors])
y = np.array(Avg_comb).T
#Y = np.array([[y,1] for y in np.linspace(5,10,10)]).reshape(2,1)
w = np.linalg.inv((X.T)@X)@(X.T)@y
plt.scatter(colors,Avg_comb)
C = np.linspace(5,10,10)
eq = "y = " + str(np.round(w[0],2)) + "x" + " + " + "("+str(np.round(w[1],2))+")"
plt.plot(C,C*w[0]+w[1])
plt.suptitle(eq)
plt.xlabel("Color Count")
plt.ylabel("Average Combinations evaluated (7 slots)")
plt.show()

print(Avg_guess)
print(Avg_comb)
