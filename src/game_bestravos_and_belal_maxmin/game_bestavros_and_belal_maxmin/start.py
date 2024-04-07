from GameHelper import GameHelper
import math
import copy
import time

# Creating gamehelper object and defining parameters
gameHelper = GameHelper()
code_length = 4
num_colors = 6

avg_guesses = 0
start_time = time.time()

for run in range(100):
    secret_code = gameHelper.generate_random_code(num_colors, code_length)
    print("Secret code:", secret_code)

    # Creating guess list
    guesses = [[a, b, c, d] for a in range(1, 7) for b in range(1, 7) for c in range(1, 7) for d in range(1, 7)]

    # Keeping track of guesses
    Guess_List = []

    # Best initial guess according to the paper
    initial_guess = [1, 1, 2, 2]
    Guess_List.append(tuple(initial_guess))
    pool = guesses

    # Generating a response to the guess
    guess = initial_guess
    no_black_pegs, no_white_pegs = 0, 0

    while not (no_black_pegs == 4 and no_white_pegs == 0):
        no_black_pegs, no_white_pegs = gameHelper.hint([guess, secret_code, code_length, num_colors])[0], gameHelper.hint([guess, secret_code, code_length, num_colors])[1]

        new_pool = []

        # Creating a guess pool
        for g in pool:
            black_pegs, white_pegs = gameHelper.hint([g, guess, code_length, num_colors])[0], gameHelper.hint([g, guess, code_length, num_colors])[1]
            if black_pegs == no_black_pegs and white_pegs == no_white_pegs:
                new_pool.append(tuple(g))

        min_info_gain = {}

        for g in new_pool:
            # Creating response dictionary
            responses = {}
            temp_pool = copy.deepcopy(new_pool)

            for g1 in temp_pool:
                black_pegs, white_pegs = gameHelper.hint([g1, g, code_length, num_colors])[0], gameHelper.hint([g1, g, code_length, num_colors])[1]
                if (black_pegs, white_pegs) not in responses:
                    responses[(black_pegs, white_pegs)] = [g1]
                else:
                    responses[(black_pegs, white_pegs)].append(g1)

            # Calculating the amount of information for each response
            information = gameHelper.calculate_information(responses, temp_pool)

            # Sorting information and appending minimum information 
            sorted_info = list(sorted(information.values()))
            if len(sorted_info) != 0:
                min_info_gain[g] = sorted_info[0]

        sorted_min_info = list(sorted(min_info_gain.values(), reverse=True))
        
        for g in min_info_gain:
            if min_info_gain[g] == sorted_min_info[0]:
                guess = g

        if tuple(guess) not in Guess_List:
            Guess_List.append(tuple(guess))
        pool = new_pool

    print(Guess_List)
    print("Number of guesses:", len(Guess_List))
    print()
    avg_guesses += len(Guess_List)

end_time = time.time()
print(avg_guesses/100)
elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time/100, "seconds")