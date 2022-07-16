class Card:
    def __init__(self, color, number, power, isNumber = False, isAction = False, isWild = False):
        self.color = color
        self.number = number
        self.power = power
        self.isNumber = isNumber
        self.isAction = isAction
        self.isWild = isWild

    def print(self):
        print(self.color, str(self.number), self.power)

