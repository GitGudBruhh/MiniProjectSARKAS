import copy
import itertools
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

    def createAnswerList(self, noColours: int, noSlots: int):
        finalAnswerList = []
        for color in range(1, noColours+1):
            finalAnswerList.append([str(color)])

        for idx in range(noSlots-1):
            tempList = []
            for elem in finalAnswerList:
                for color in range(1, noColours+1):
                    newElem = copy.copy(elem)
                    newElem.append(str(color))
                    tempList.append(newElem)
            finalAnswerList = tempList

        return finalAnswerList

    def createScoreDictionary(self, noColours: int, noSlots: int):
        answerList = self.createAnswerList(noColours, noSlots)
        scoreDict = {}
        for elem in answerList:
            scoreDict[elem] = []

    @staticmethod
    def initialize_possible_answers(noColours: int, noSlots: int):
        return list(itertools.product(range(1, noColours+1), repeat=noSlots))

    @staticmethod
    def score_guess(guess, secret):
        black = sum(g == s for g, s in zip(guess, secret))
        white = sum(min(guess.count(j), secret.count(j)) for j in set(guess)) - black
        return black, white

    @staticmethod
    def reduce_possible_answers(possible_answers, last_guess, last_score):
        return [answer for answer in possible_answers if GameHelper.score_guess(last_guess, answer) == last_score]

    @staticmethod
    def choose_next_guess(possible_answers, all_combinations):
        min_max_score = len(possible_answers)
        next_guess = possible_answers[0]
        for guess in all_combinations:
            score_counts = {}
            for answer in possible_answers:
                score = GameHelper.score_guess(guess, answer)
                if score in score_counts:
                    score_counts[score] += 1
                else:
                    score_counts[score] = 1
            max_score = max(score_counts.values())
            if max_score < min_max_score:
                min_max_score = max_score
                next_guess = guess
        return next_guess
