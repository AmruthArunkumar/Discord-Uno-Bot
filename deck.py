from card import Card
from player import Player
from random import shuffle as sh
from pile import Pile
import game

maxPeople = 6

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
        cards = cards + cards + cards
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

    def print(self, sprites):
        handString = ""
        index = 0
        for card in self.cards:
            print(card.color, card.power)
            handString += card.toString(sprites)
            if index != (len(self.cards) - 1):
                handString += "\n"
            index += 1
        return handString        

    def distribute(self, people):
        playerList = []
        i = 0
        for person in people:
            hand = self.cards[:7]
            del self.cards[:7]
            playerList.append(Player(str(person), i, hand))
            i += 1
        isNumber = False
        index = -1
        while not isNumber:
            index += 1
            topCard = self.cards[index]
            isNumber = topCard.isNumber
        del self.cards[index]
        self.initPile(topCard)
        return playerList
    
    def initPile(self, topCard):
        game.pile = Pile(topCard)
