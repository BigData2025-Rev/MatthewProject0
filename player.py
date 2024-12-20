from statistics import mode
from deck import Deck, Card

class Player:
    def __init__(self, d,):
        self.cards = []
        self.deck = d
        self.selected = []

    def draw(self,n):
        for card in self.deck.draw(n):
            self.cards.append(card)
        self.cards.sort(key = lambda c : c.getRank())

    def select(self, i):
        self.selected.append(self.cards.pop(i))
    def discard(self):
        for _ in self.selected:
            self.deck.discards.append(self.selected.pop())

    def setCards(self, cards):
        self.cards = cards

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
            


player = Player(Deck())
player.draw(5)
player.displayCards()
print(player.scoreHand())