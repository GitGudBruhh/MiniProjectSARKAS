import copy
import random
from GameData import GameData

class GameHelper:

    def createSecretCode(self, noColours: int, noSlots: int):
        secretCode = []
        colourRange = list(range(1,noColours+1))
        for i in range(noSlots):
            secretCode.append(str(random.choice(colourRange)))

        print(secretCode)
        return secretCode

    def isValidGuess(self, gameData: GameData, playerGuess: list[str]):
        if not (len(playerGuess) == gameData.getNoSlots()):
            print("Length of guess not equal to number of slots")
            return False

        colourRange = list(range(1, gameData.getNoColours() + 1))
        for colour in playerGuess:
            if not int(colour) in colourRange:
                print("Guess values out of range")
                return False

        return True
