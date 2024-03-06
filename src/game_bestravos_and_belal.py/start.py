from GameHelper import GameHelper
import math

# Creating gamehelper object and defining parameters
gameHelper = GameHelper()
code_length = 4
num_colors = 6

# Creating guess list
guesses = [[a, b, c, d] for a in range(1, 7) for b in range(1, 7) for c in range(1, 7) for d in range(1, 7)]
guesses.remove([1,1,2,2])

# Best initial guess according to the paper
initial_guess = [1, 1, 2, 2]

# Creating response dictionary
responses = {}

for guess in guesses:
    black_pegs, white_pegs = gameHelper.hint([guess, initial_guess, code_length, num_colors])[0], gameHelper.hint([guess, initial_guess, code_length, num_colors])[1]
    if (black_pegs, white_pegs) not in responses:
        responses[(black_pegs, white_pegs)] = [guess]
    else:
        responses[(black_pegs, white_pegs)].append(guess)

# Calculating the amount of information for each response
information = gameHelper.calculate_information(responses, guesses)

# Sorting the information in ascending order
sorted_info = list(sorted(information.values(), reverse=True))

for info in information:
    if information[info] == sorted_info[0]:
        next_guess = responses[info][0]

print(next_guess)