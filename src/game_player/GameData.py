import copy

class GameData:
    noColours = None
    maxGuesses = None
    noSlots = None
    secretCode = None

    def __init__(self, noColours: int, maxGuesses: int, noSlots: int, secretCode: list[str]):
        # print(noColours)
        self.setNoColours(noColours)
        self.setMaxGuesses(maxGuesses)
        self.setNoSlots(noSlots)
        self.setSecretCode(copy.copy(secretCode))

    def getNoColours(self):
        return self.noColours

    def getMaxGuesses(self):
        return self.maxGuesses

    def getNoSlots(self):
        return self.noSlots

    def getSecretCode(self):
        return copy.copy(self.secretCode)

    def setNoColours(self, noColours: int):
        self.noColours = noColours

    def setMaxGuesses(self, maxGuesses: int):
        self.maxGuesses = maxGuesses

    def setNoSlots(self, noSlots: int):
        self.noSlots = noSlots

    def setSecretCode(self, secretCode: list[str]):
        self.secretCode = secretCode
