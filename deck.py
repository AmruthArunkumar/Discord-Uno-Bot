from card import Card
from player import Player
from random import shuffle as sh

maxPeople = 10

class Deck:
    def __init__(self):
        self.cards = self.createNew()
        self.shuffle()

    def createNew(self):
        cards = []
        cards += self.addColored("green")
        cards += self.addColored("yellow")
        cards += self.addColored("red")
        cards += self.addColored("blue")
        cards += self.addWilds()
        return cards

    def printAll(self):
        for card in self.cards:
            card.print()
        
    def shuffle(self):
        sh(self.cards)
    
    def addColored(self, color):
        coloredCards = []
        coloredCards.append(Card(color, 0, None, isNumber = True))
        for i in range(9):
            num = i + 1
            coloredCards.append(Card(color, num, None, isNumber = True))
            coloredCards.append(Card(color, num, None, isNumber = True))
        for type in ["+2", "skip", "reverse"]:
            coloredCards.append(Card(color, None, type, isAction = True))
            coloredCards.append(Card(color, None, type, isAction = True))
        return coloredCards

    def addWilds(self):
        wildCards = []
        for type in ["+4", "wild"]:
            for i in range(4):
                wildCards.append(Card("black", None, type, isWild = True))
        return wildCards

    def distribute(self, people):
        pass