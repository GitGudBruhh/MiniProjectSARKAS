import copy
from GameData import GameData

class GameState:
    gameData = None
    playGrid = None
    hintGrid = None
    currentGuessNo = 0
    isComplete = False
    isWin = False

    def __init__(self, gameData: GameData):
        noSlots = gameData.getNoSlots()
        maxGuesses = gameData.getMaxGuesses()
        self.setGameData(gameData)
        self.initPlayGrid(noSlots, maxGuesses)
        self.initHintGrid(noSlots, maxGuesses)

    def getGameData(self):
        return copy.deepcopy(self.gameData)

    def setGameData(self, gameData: GameData):
        self.gameData = gameData

    def getCurrentGuessNo(self):
        return self.currentGuessNo

    def setCurrentGuess(self, currentGuessNo: int):
        self.currentGuessNo = currentGuessNo

    def isGameComplete(self):
        return self.isComplete

    def setGameComplete(self):
        self.isComplete = True

    def isGameWon(self):
        return self.isWin

    def setGameWon(self):
        self.isWin = True

    def getPlayGrid(self):
        return self.playGrid

    def getHintGrid(self):
        return self.hintGrid

    def initPlayGrid(self, noSlots: int, maxGuesses: int):
        newGrid = []
        for rowNumber in range(maxGuesses):
            newRow = ["_"]*noSlots
            newGrid.append(newRow)

        self.playGrid = newGrid

    def initHintGrid(self, noSlots: int, maxGuesses: int):
        newGrid = []
        for rowNumber in range(maxGuesses):
            newRow = ["."]*noSlots
            newGrid.append(newRow)

        self.hintGrid = newGrid

    def displayPlayGrid(self):
        for row in self.playGrid:
            print(" ".join(row))

    def displayHintGrid(self):
        for row in self.HintGrid:
            print(" ".join(row))

    def displayAllGrid(self):
        noRows = self.gameData.getMaxGuesses()
        for i in range(noRows):
            print(" ".join(self.playGrid[i]) + "      " + " ".join(self.hintGrid[i]))

    def updatePlayGrid(self, currentGuess: list[str]):
        #checkValidCode()
        self.playGrid[self.currentGuessNo] = currentGuess

    def updateHintGrid(self, currentGuess: list[str]):
        secretCode = (self.gameData.getSecretCode()).copy()
        noCorrectColours = 0
        noCorrectPlacements = 0

        for elem in currentGuess:
            if elem in secretCode:
                noCorrectColours += 1
                secretCode.pop(secretCode.index(elem))

        secretCode = (self.gameData.getSecretCode()).copy()
        noSlots = self.gameData.getNoSlots()

        for idx in range(noSlots):
            if currentGuess[idx] == secretCode[idx]:
                noCorrectPlacements += 1

        noWrongPlacements = noCorrectColours - noCorrectPlacements

        hint = ["O"]*noCorrectPlacements + ["X"]*noWrongPlacements + ["."]*(noSlots - noCorrectColours)
        self.hintGrid[self.currentGuessNo] = hint

    def playGuessAndUpdateState(self, currentGuess: list[str]):
        self.updatePlayGrid(currentGuess)
        self.updateHintGrid(currentGuess)
        self.currentGuessNo += 1

        maxGuesses = self.gameData.getMaxGuesses()
        if(self.currentGuessNo == maxGuesses):
            self.setGameComplete()
        secretCode = self.gameData.getSecretCode()
        if currentGuess == secretCode:
            self.setGameWon()
            self.setGameComplete()

        print(self.isGameComplete)
        print(self.isGameWon)
