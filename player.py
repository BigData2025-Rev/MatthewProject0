from statistics import mode
from deck import Deck, Card

class Player:
    def __init__(self, deck, chips = 0):
        self.cards = []
        self.deck = deck
        self.selected = []
        self.chips = chips

    def draw(self,n):
        for card in self.deck.draw(n):
            self.cards.append(card)
        self.cards.sort(key = lambda c : c.getRank())

    def select(self, card):
        self.selected.append(card)
    def discard(self):
        for card in self.selected:
            self.deck.discards.append(self.cards.pop(self.cards.index(card)))
        self.draw(len(self.selected))
        self.selected = []

    def discardAll(self):
        while len(self.cards) > 0:
            self.deck.discards.append(self.cards.pop())

    def setCards(self, cards):
        self.cards = cards
    def getChips(self):
        return self.chips
    def addChips(self, chips):
        self.chips += chips

    def scoreHand(self):
        #Checks for flushes, straights, then matching ranks, beginning with 4s of a kind and full houses
        #returns hand type and highest scoring card
        ranks = [c.getRank() for c in self.cards]
        suits = [c.getSuit() for c in self.cards]

        if suits.count(suits[0]) == 5:
            #Accounting for A2345 straight
            if ranks == [1,2,3,4,13]:
                return ["straight flush",4]
            for i in range(4):
                if ranks[i] != ranks[i+1] - 1:
                    return ["flush", max(ranks)]
                return ["straight flush", max(ranks)]

        for i in range(4):
            if ranks[i] != ranks[i+1] - 1:
                break
            if i == 3:
                return ["straight",max(ranks)]

        if ranks == [1,2,3,4,13]:
            return ["straight", 4]

        counts = []
        for r in ranks:
            count = ranks.count(r)
            counts.append(count)
        for r in ranks:
            if 4 in counts:
                return ["four of a kind", mode(ranks)]
            elif 3 in counts:
                if 2 in counts:
                    return ["full house", mode(ranks)]
                else: return ["three of a kind", mode(ranks)]
            elif 2 in counts:
                if counts.count(2) > 2:
                    filteredRanks = [r for r in ranks if ranks.count(r) == 2]
                    return ["two pair", max(filteredRanks)]
                else: return ["pair", mode(ranks)]
        return ["high card", max(ranks)]
    def displayCards(self):
        for row in range(11):
            
            for card in self.cards:
                print(card.getFace()[row], end= " ")
            print("\n", end="")
            

