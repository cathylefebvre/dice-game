import dice as d
import score as s


class Player:
    categories = ["ones", "twos", "threes", "fours", "fives", "sixes", "bonus", "Three of a kind",
                  "Four of a kind", "Full house", "Small straight", "Large straight", "Chance", "Yahtzee"]
    topHalfCategories =["ones", "twos", "threes", "fours", "fives", "sixes"]
    bottomHalfCategories = ["Chance", "Three of a kind", "Four of a kind", "Full house",
                            "Small straight", "Large straight", "Yahtzee"]
    die = d.dice()

    def __init__(self, name="", ai_num = 0):
        self.name = name
        if self.name is "":
            self.name = "AI "
            self.name += str(ai_num)
        self.scores = {x: -1 for x in Player.categories}
        self.total = 0
        self.dieScore = s.score(Player.die.setOfDie)
        self.topHalfTotal = 0

    def total_score(self):
        self.total = 0
        for x in ["ones", "twos", "threes", "fours", "fives", "sixes"]:
            if self.scores[x] is not -1:
                self.total += self.scores[x]
        if self.total > 63:
            if self.scores["bonus"] is -1:
                self.scores["bonus"] = 35
            else:
                self.scores["bonus"] += 35
        for x in ["bonus", "Three of a kind", "Four of a kind", "Full house",
                  "Small straight", "Large straight", "Chance", "Yahtzee"]:
            if self.scores[x] is not -1:
                self.total += self.scores[x]
        return self.total

    def print_score_card(self):
        print("---")
        for x in Player.categories:
            if self.scores[x] is -1:
                print("%s:  ---" % (x))
            else:
                print("%s:  %i" % (x, self.scores[x]))
        print(self.total)
        print("---")

    def take_turn(self, turn):
        print(" It is now turn %i for %s." % (turn+1, self.name))
        Player.die.print_set()
        self.select_die()
        Player.die.print_set()
        self.select_die()
        Player.die.print_set()
        self.dieScore = s.score(Player.die.setOfDie)
        # check if bonus Yahtzee
        if Player.die.setOfDie.count(Player.die.setOfDie[1]) is 5 and self.scores["Yahtzee"] is 50:
            if self.scores["bonus"] is -1:
                self.scores["bonus"] = 100
            else:
                self.scores["bonus"] += 100
        self.select_score()
        self.print_score_card()
        Player.die.roll_nums()

    def select_die(self):
        nums = raw_input("Which dice do you want to re-roll?  (press enter to not re-roll any die)")
        Player.die.roll_nums(nums)

    def select_score(self):
        scored = False
        while not scored:
            print("You can score ---")
            self.dieScore.print_score(self)
            try:
                category = int(raw_input("Which do you want to score?"))
            except ValueError as e:
                print "Error must type in a number value"
            if category is 0:
                j = 1
                for x in self.dieScore.zero:
                    print("#%i -- %s" % (j, x))
                    j += 1
                try:
                    int_for_zero = int(raw_input("Which do you want to score? (0 to return to other scoring options)"))
                except ValueError as e:
                    print "Error must type in a number value"
                j = 1
                for x in self.dieScore.zero:
                    if int_for_zero is j:
                        self.scores[x] = 0
                        scored = True
                        break
                    j += 1
            i = 1
            for x in self.dieScore.categories:
                if self.dieScore.scores[x] > 0 and self.scores[x] is -1:
                    if category is i:
                        self.scores[x] = self.dieScore.scores[x]
                        scored = True
                        self.total += self.dieScore.scores[x]
                        if category in [Player.topHalfCategories]:
                            if self.topHalfTotal < 63:
                                self.topHalfTotal += self.dieScore.scores[x]
                                if self.topHalfTotal < 63:
                                    if self.scores["bonus"] is -1:
                                        self.scores["bonus"] = 35
                                    else:
                                        self.scores["bonus"] += 35
                        break
                    i += 1

class AI(Player):
    def select_die(self):
        self.dieScore = s.score(Player.die.setOfDie)
        count = {}
        replace = []
        for i in range(1, 7):
            count.update({i: Player.die.setOfDie.count(i)})
        print count
        if self.dieScore.scores["Large straight"] > 0 and self.scores["Large straight"] is -1:
            Player.die.ai_roll([])
        if self.dieScore.scores["Small straight"] > 0 and (self.scores["Large straight"] is -1 or self.scores["Large straight"] is -1):
            if 2 in count.values():
                for i in count.keys():
                    if count[i] is 2:
                        Player.die.ai_roll([i])
        if self.dieScore.scores["Full house"] > 0 and self.scores["Full house"] is -1:
            Player.die.ai_roll([])
        straight = []
        last = 0
        for i in range(1, 7):
            if len(straight) is 0:
               straight.append(i)
            elif straight[len(straight)-1] + 1 is i:
                straight.append(i)
            elif len(straight) < 3:
                straight = [i]
        if len(straight) >= 4:
            for i in Player.die.setOfDie:
                if i not in straight:
                    replace.append(i)
            Player.die.ai_roll(replace)
        if 3 in count.values() or 4 in count.values():
            keep = 0
            for (num, c) in count.items():
                if c >= 3:
                    keep = num
            for i in Player.die.setOfDie:
                if i is not keep:
                    replace.append(i)
            Player.die.ai_roll(replace)
        if len(straight) is 3:
            for i in Player.die.setOfDie:
                if i not in straight:
                    replace.append(i)
            Player.die.ai_roll(replace)
        if self.dieScore.scores["Yahtzee"] > 0:
            Player.die.roll_nums([])

    def select_score(self):
        best_category = ""
        bestScore = 0
        for x in Player.bottomHalfCategories:
            if self.dieScore.scores[x] >= bestScore and self.scores[x] is -1:
                bestScore = self.dieScore.scores[x]
                best_category = x
                print x
        bestCount = 0
        if best_category is "Chance" or "":
            for i in range(1, 7):
                if Player.die.setOfDie.count(i) > bestCount and self.scores[Player.categories[i-1]] is -1:
                    best_category = Player.categories[i-1]
                    bestCount = Player.die.setOfDie.count(i)

        if bestCount is 0 and bestScore is 0:
            # score zero in the first available category
            for x in Player.categories:
                if self.scores[x] is -1 and x is not "bonus":
                    best_category = x

        self.scores[best_category] = self.dieScore.scores[best_category]
        self.total += self.dieScore.scores[best_category]
        if best_category in [Player.topHalfCategories]:
            if self.topHalfTotal < 63:
                self.topHalfTotal += self.dieScore.scores[x]
                if self.topHalfTotal > 63:
                    if self.scores["bonus"] is -1:
                        self.scores["bonus"] = 35







