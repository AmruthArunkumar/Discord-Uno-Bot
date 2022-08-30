from turtle import color


class Card:
    def __init__(self, color, number, power, isNumber = False, isAction = False, isWild = False):
        self.color = color
        self.number = number
        self.power = power
        self.isNumber = isNumber
        self.isAction = isAction
        self.isWild = isWild

    def toString(self, sprites):
        if self.isNumber:
            return f"<:{sprites[self.color].name}:{sprites[str(self.color)].id}> <:{sprites[str(self.number)].name}:{sprites[str(self.number)].id}> ({self.color} {str(self.number)})"
        elif self.isAction:
            return f"<:{sprites[self.color].name}:{sprites[str(self.color)].id}> <:{sprites[self.power].name}:{sprites[self.power].id}> ({self.color} {self.power})"
        elif self.isWild:
            if self.power == "wild":
                if self.color == "black":
                    return f"<:{sprites[self.power].name}:{sprites[self.power].id}> ({self.power})"
                else:
                    return f"<:{sprites[self.color].name}:{sprites[self.color].id}> ({self.color} {self.power})"
            elif self.power == "+4":
                if self.color == "black":
                    return f"<:{sprites[self.power].name}:{sprites[self.power].id}> ({self.power})"
                else:
                    emoji = self.color + self.power
                    return f"<:{sprites[emoji].name}:{sprites[emoji].id}> ({self.color} {self.power})"
            
