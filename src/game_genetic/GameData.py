import copy

class GameData:
    noColours = None
    maxGuesses = None
    noSlots = None
    secret_code = None
    POPULATION_SIZE=None
    NUM_GENERATIONS=None
    MUTATION_RATE=None

    # CODE_LENGTH = 6  # Length of the secret code
    # NUM_COLORS = 8   # Number of different colors
    # POPULATION_SIZE = 100  # Size of the population
    # NUM_GENERATIONS = 500   # Maximum number of generations to evolve
    # MUTATION_RATE = 0.1    # Probability of mutation

    def __init__(self, NUM_COLORS: int, POPULATION_SIZE: int, CODE_LENGTH: int, secret_code: list[str], NUM_GENERATIONS: int, MUTATION_RATE: float):
        # print(noColours)
        self.setNoColours(NUM_COLORS)
        self.setPopSize(POPULATION_SIZE)
        self.setNoSlots(CODE_LENGTH)
        self.setSecretCode(copy.copy(secret_code))
        self.setNumGen(NUM_GENERATIONS)
        self.setMutRate(MUTATION_RATE)

    def getNoColours(self):
        return self.NUM_COLORS

    def getPopSize(self):
        return self.POPULATION_SIZE
    
    def getNumGen(self):
        return self.NUM_GENERATIONS
    
    def getMutRate(self):
        return self.MUTATION_RATE

    def getNoSlots(self):
        return self.CODE_LENGTH

    def getSecretCode(self):
        return copy.copy(self.secret_code)

    def setNoColours(self, NUM_COLORS: int):
        self.NUM_COLORS = NUM_COLORS
        
    def setPopSize(self, POPULATION_SIZE: int):
        self.POPULATION_SIZE=POPULATION_SIZE
    
    def setNumGen(self, NUM_GENERATIONS: int):
        self.NUM_GENERATIONS=NUM_GENERATIONS

    def setMutRate(self, MUTATION_RATE: float):
        self.MUTATION_RATE= MUTATION_RATE

    def setNoSlots(self, CODE_LENGTH: int):
        self.CODE_LENGTH = CODE_LENGTH

    def setSecretCode(self, secret_code: list[str]):
        self.secret_code = secret_code
