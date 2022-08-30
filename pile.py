class Pile:
    def __init__(self, currentCard):
        self.currentCard = currentCard
        self.stack = [self.currentCard]
    
    def addCard(self, card):
        self.currentCard = card
        self.stack.append(card)