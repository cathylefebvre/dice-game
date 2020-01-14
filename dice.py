import random as r
class dice():
    def __init__(self):
        self.setOfDie = []
        for x in range(1, 6):
            self.setOfDie.append(r.randint(1,6))
        self.setOfDie.sort()

    def print_set(self):
        print("---")
        print("DICE ROLL: ")
        for x in range(1, 7):
            row = ""
            for y in range(1, 6):
                if (x is 6):
                    row += (' *Dice #%i: %i* ' %(y, self.setOfDie[y-1]))
                if (x is 1):
                    row += ("  +-------+   ")
                if (x is 2):
                    if (self.setOfDie[y-1] is 4) or (self.setOfDie[y-1] is 5) or (self.setOfDie[y-1] is 6):
                        row += ("  | 0   0 |   ")
                    else:
                        row += ("  | 0     |   ")
                if (x is 3):
                    if (self.setOfDie[y-1] is 6):
                        row += ("  | 0   0 |   ")
                    else:
                        if (self.setOfDie[y-1] is 3) or (self.setOfDie[y-1]is 5):
                            row += ("  |   0   |   ")
                        else:
                            row += ("  |       |   ")
                if (x is 4):
                    if (self.setOfDie[y-1] is 4) or (self.setOfDie[y-1] is 5) or (self.setOfDie[y-1] is 6):
                        row += ("  | 0   0 |   ")
                    else:
                        if (self.setOfDie[y-1] is 2) or (self.setOfDie[y-1]is 3):
                            row += ("  |     0 |   ")
                        else:
                            row += ("  |       |   ")
                if (x is 5):
                    row += ("  +-------+   ")
            print(row)
        print("---")

    def roll_nums(self, numSet ="12345"):
        for x in range(0, 5):
            if str(x+1) in numSet:
                self.setOfDie.pop(x)
                self.setOfDie.insert(x, r.randint(1,6))
        self.setOfDie.sort()
