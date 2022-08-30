import interactions

class Player:
    def __init__(self, name: interactions.User, turnNumber, hand):
        self.name = name
        self.turnNumber = turnNumber
        self.hand = hand
        self.hasDrawn = False
        self.hasToDraw = False
        self.isUnoCalled = False

    def useCard(self, color, type):
        inHand = False
        index = 0
        i = 0
        if color not in ["red", "blue", "green", "yellow"]:
            return -2
        if type not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+2", "+4", "wild", "skip", "reverse"]:
            return -2
        for card in self.hand:
            if card.color == color and (str(card.number) == type or card.power == type):
                inHand = True
                index = i
            elif (card.power == "wild" and type == "wild") or (card.power == "+4" and type == "+4"):
                inHand = True
                index = i
            i += 1
        if inHand:
            return index
        else:
            return -1
        
    def isFinished(self):
        return True if len(self.hand) <= 0 else False
    
    def printHand(self, sprites):
        handString = ""
        index = 0
        for card in self.hand:
            if card.isWild:
                if card.color != "black":
                    card.color == "black"
            handString += card.toString(sprites)
            if index != (len(self.hand) - 1):
                handString += "\n"
            index += 1
        return handString
        