import os
import time
import copy
from GameData import GameData
from GameState import GameState
from GameHelper import GameHelper

# For games with more than six colours, it is not known what the smallest
# number of guesses is to crack any possible code

def playGame():

    gameHelper = GameHelper()
    while(1):
        # noColours = int(input("Enter number of colours: "))
        # noSlots = int(input("Enter number of columns: "))
        # maxGuesses = int(input("Enter maximum number of guesses allowed: "))
        # secretCode = gameHelper.createSecretCode(noColours, noSlots)

        noColours = 6
        noSlots = 4
        maxGuesses = 10
        secretCode = gameHelper.createSecretCode(noColours, noSlots)

        newGameData = GameData(noColours, maxGuesses, noSlots, secretCode)
        newGameState = GameState(newGameData)

        playAgain = "N"
        os.system("clear")
        newGameState.displayAllGrid()

        while(not newGameState.isGameWon()):
            # aiGuessStr = input("\n\nEnter your guess:\n\n")
            # aiGuess = aiGuessStr.split(" ")
            aiGuess = ["1", "1", "2", "2"]

            # TODO:
            isValidGuess = gameHelper.isValidGuess(newGameData, aiGuess)
            if not isValidGuess:
                continue

            newGameState.playGuessAndUpdateState(aiGuess)
            os.system("clear")

            #TODO:
            #newGameState.updateScore()
            #print(newGameState.getScore(), "\n\n")

            newGameState.displayAllGrid()
            time.sleep(2)

            if newGameState.isGameComplete():
                if newGameState.isGameWon():
                    print("\n\nAI Wins!")
                else:
                    print("\n\nAI Lost")
                    print("Secret code was: ", " ".join(newGameData.getSecretCode()))

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
