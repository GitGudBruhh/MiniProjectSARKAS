import tkinter as tk
from tkinter import messagebox
import random
from GameHelper import GameHelper

# Main genetic algorithm with parallel fitness calculation
def genetic_algorithm(secret_code, numColors, codeLength, populationSize, numGenerations, mutationRate, permutationRate, inversionRate):
    i = 0
    gameHelper = GameHelper()
    Intial_Guess = gameHelper.generate_random_code(numColors, codeLength)
    args = (Intial_Guess, secret_code, codeLength, numColors)
    pegs = gameHelper.hint(args)
    Guess_List = [[Intial_Guess, gameHelper.hint((Intial_Guess, secret_code, codeLength, numColors))]]
    while (pegs[0] != codeLength):
        i += 1
        h = 1
        Eligible_set = set()
        population = [gameHelper.generate_random_code(numColors, codeLength) for _ in range(populationSize)]

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

            population_with_fitness = list(zip(fitness_list, population))
            population_with_fitness.sort(key=lambda x: x[0])
            for k in range(len(population_with_fitness)):
                if len(Eligible_set) >= populationSize:
                    break
                if population_with_fitness[k][0] == 2 * codeLength * (len(Guess_List) - 1) and tuple(
                        population_with_fitness[k][1]) not in Eligible_set:
                    Eligible_set.add(copy.deepcopy(tuple(population_with_fitness[k][1])))

            h += 1

        try:
            Random_Guess = random.choice(list(Eligible_set))
        except:
            messagebox.showinfo("Result", "Algorithm did not find the secret code within the maximum generations")
            return

        Guess_List.append(
            copy.deepcopy([Random_Guess, tuple(gameHelper.hint((Random_Guess, secret_code, codeLength, numColors)))]))
        a = (Random_Guess, secret_code, codeLength, numColors)
        pegs = gameHelper.hint(a)

    print(f"Solution found: {Guess_List[-1]}")
    print("Number of Guesses:", len(Guess_List))
    return Guess_List[-1]

# Function to check the guess
# def check_guess():
#     global count
#     guess = genetic_algorithm(secret_code, NUM_COLORS, CODE_LENGTH, POPULATION_SIZE, NUM_GENERATIONS, 0.03, 0.03, 0.02)
#     args = (guess, secret_code, CODE_LENGTH, NUM_COLORS)
#     pegs = gameHelper.hint(args)
#     if pegs[0] == CODE_LENGTH:
#         messagebox.showinfo("Result", "You guessed the code!")
#         reset_game()
#     else:
#         count += 1
#         if count >= NUM_GENERATIONS:
#             messagebox.showinfo("Result", f"Out of guesses! The secret code was {secret_code}")
#             reset_game()
#         else:
#             messagebox.showinfo("Result", f"Wrong guess! You have {NUM_GENERATIONS - count} guesses left.")

# # Function to reset the game
# def reset_game():
#     global count, secret_code
#     secret_code = gameHelper.generate_random_code(NUM_COLORS, CODE_LENGTH)
#     count = 0

# # Create the main window
# root = tk.Tk()
# root.title("Mastermind Game")

# # Generate a secret code
# gameHelper = GameHelper()
# CODE_LENGTH = 4
# NUM_COLORS = 6
# POPULATION_SIZE = 150
# NUM_GENERATIONS = 10
# secret_code = gameHelper.generate_random_code(NUM_COLORS, CODE_LENGTH)
# count = 0

# # Create entry widgets for the guesses
# entry1 = tk.Entry(root, width=3)
# entry1.grid(row=0, column=0)
# entry2 = tk.Entry(root, width=3)
# entry2.grid(row=0, column=1)
# entry3 = tk.Entry(root, width=3)
# entry3.grid(row=0, column=2)
# entry4 = tk.Entry(root, width=3)
# entry4.grid(row=0, column=3)

# # Create a button to submit the guess
# submit_button = tk.Button(root, text="Submit Guess", command=check_guess)
# submit_button.grid(row=1, column=1, columnspan=2)

# # Run the main event loop
# root.mainloop()

def check_guess():
    global count
    guess = genetic_algorithm(secret_code)
    if guess == secret_code:
        messagebox.showinfo("Result", "You guessed the code!")
        reset_game()
    else:
        count += 1
        if count >= NUM_GENERATIONS:
            messagebox.showinfo("Result", f"Out of guesses! The secret code was {secret_code}")
            reset_game()
        else:
            messagebox.showinfo("Result", f"Wrong guess! You have {NUM_GENERATIONS - count} guesses left.")

# Function to reset the game
def reset_game():
    global count, secret_code
    secret_code = generate_secret_code()
    count = 0

# Generate a secret code
def generate_secret_code():
    return [random.randint(1, 6) for _ in range(CODE_LENGTH)]

# Initialize global variables
CODE_LENGTH = 4
NUM_GENERATIONS = 10
secret_code = generate_secret_code()
count = 0

# Create the main window
root = tk.Tk()
root.title("Mastermind Game")

# Increase the size of the main window
root.geometry("400x200")

# Create entry widgets for the guesses
entry1 = tk.Entry(root, width=5, font=("Helvetica", 16))  # Increase font size
entry1.grid(row=0, column=0)
entry2 = tk.Entry(root, width=5, font=("Helvetica", 16))  # Increase font size
entry2.grid(row=0, column=1)
entry3 = tk.Entry(root, width=5, font=("Helvetica", 16))  # Increase font size
entry3.grid(row=0, column=2)
entry4 = tk.Entry(root, width=5, font=("Helvetica", 16))  # Increase font size
entry4.grid(row=0, column=3)

# Create a button to submit the guess
submit_button = tk.Button(root, text="Submit Guess", command=check_guess, font=("Helvetica", 14))  # Increase font size
submit_button.grid(row=1, column=1, columnspan=2)

# Run the main event loop
root.mainloop()
