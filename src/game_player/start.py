import os
import copy
from GameData import GameData
from GameState import GameState
from GameHelper import GameHelper

def playGame():

    gameHelper = GameHelper()
    while(1):
        noColours = int(input("Enter number of colours: "))
        maxGuesses = int(input("Enter maximum number of guesses allowed: "))
        noSlots = int(input("Enter number of columns: "))
        secretCode = gameHelper.createSecretCode(noColours, noSlots)

        newGameData = GameData(noColours, maxGuesses, noSlots, secretCode)
        newGameState = GameState(newGameData)

        playAgain = "N"
        os.system("clear")
        newGameState.displayAllGrid()

        while(not newGameState.isGameWon()):
            playerGuessStr = input("\n\nEnter your guess:\n\n")
            playerGuess = playerGuessStr.split(" ")

            # TODO:
            isValidGuess = gameHelper.isValidGuess(newGameData, playerGuess)
            if not isValidGuess:
                continue

            newGameState.playGuessAndUpdateState(playerGuess)
            os.system("clear")

            #TODO:
            #newGameState.updateScore()
            #print(newGameState.getScore(), "\n\n")

            newGameState.displayAllGrid()

            if newGameState.isGameComplete():
                if newGameState.isGameWon():
                    print("\n\nPlayer Wins!")
                else:
                    print("\n\nPlayer Lost")
                    print("Secret code was: ", " ".join(newGameData.getSecretCode()))

                playAgain = input("\nPlay Again? (Y/N):")

                while(1):

                    if not ((playAgain == "Y") or
                    (playAgain == "y") or
                    (playAgain == "N") or
                    (playAgain == "n")):
                        playAgain = input("Please enter a valid input (Y/N):")
                        continue
                    else:
                        break

                if((playAgain == "N") or
                (playAgain == "n")):
                    return
                else:
                    break
    return


##Main
playGame()

