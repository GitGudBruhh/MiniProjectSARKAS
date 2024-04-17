import os
import time
import copy
from GameData import GameData
from GameState import GameState
from GameHelper import GameHelper
import itertools

# For games with more than six colours, it is not known what the smallest
# number of guesses is to crack any possible code


def playGame():

        gameHelper = GameHelper()
        # noColours = int(input("Enter number of colours: "))
        # noSlots = int(input("Enter number of columns: "))
        # maxGuesses = int(input("Enter maximum number of guesses allowed: "))
        # secretCode = gameHelper.createSecretCode(noColours, noSlots)

        noColours = 6
        noSlots = 4
        maxGuesses = 10
        secretCode = gameHelper.createSecretCode(noColours, noSlots)
        secretCode = tuple([int(x) for x in secretCode])
        newGameData = GameData(noColours, maxGuesses, noSlots, secretCode)
        newGameState = GameState(newGameData)

        # playAgain = "N"
        # os.system("clear")
        # newGameState.displayAllGrid()


        # Setting up the variables for our 'mastermind'
        all_combinations = GameHelper.initialize_possible_answers(noColours, noSlots)
        possible_answers = all_combinations.copy()
        guess = (1, 1, 2, 2)  # Knuth's initial guess
        attempts = 0
        while(1):
            # if attempts == maxGuesses:
            #     newGameState.isGameComplete()
            attempts += 1
            # if newGameState.isGameComplete():
            #     if newGameState.isGameWon():
            #         print("\n\nAI Wins!")
            #     else:
            #         print("\n\nAI Lost")
            #         print("Secret code was: ", " ".join(newGameData.getSecretCode()))
            print(f"Attempt {attempts}: {guess}")
            if guess == secretCode:
                print(f"Guessed correctly in {attempts} attempts!")
                # newGameState.setGameWon()
                # newGameState.setGameComplete()
                break
            current_score = GameHelper.score_guess(guess, secretCode)
            possible_answers = GameHelper.reduce_possible_answers(possible_answers, guess, current_score)
            guess = GameHelper.choose_next_guess(possible_answers, all_combinations)



            # REDUNDANT:
            # isValidGuess = gameHelper.isValidGuess(newGameData, aiGuess)
            # if not isValidGuess:
            #     continue

            # newGameState.playGuessAndUpdateState(aiGuess)
            # os.system("clear")

            #REDUNDANT:
            #newGameState.updateScore()
            #print(newGameState.getScore(), "\n\n")

            # newGameState.displayAllGrid()
            # time.sleep(2)



                # playAgain = input("\nPlay Again? (Y/N):")

                # while(1):
                #
                #     if not ((playAgain == "Y") or
                #     (playAgain == "y") or
                #     (playAgain == "N") or
                #     (playAgain == "n")):
                #         playAgain = input("Please enter a valid input (Y/N):")
                #         continue
                #     else:
                #         break
                #
                # if((playAgain == "N") or
                # (playAgain == "n")):
                #     return
                # else:
                #     break
        print(f'The secret code was {secretCode}')
        return


##Main
playGame()


#                       From answerList -->
#             +----+-------------------------
#             |    |  a1  a2  a3  a4  a5  ...
# From        +----+-------------------------
# scoreDict   | g1 |  11  12  13  14  15
#   |         | g2 |  21  22  23  24  25
#   |         | g3 |  31  32  33  34  35
#   v         | g4 |  41  42  43  44  45
#             | g5 |  51  52  53  54  55
#             | .  |                    .
#             | .  |                     .
#             | .  |                      .
