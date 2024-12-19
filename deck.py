import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def getRank(self):
        return self.rank
    def getSuit(self):
        return self.suit
    def __str__(self):
        return f"{self.rank}{self.suit} "
    def getActualRank(self):
        return {1:2,2:3,3:4,5:6,6:7,8:9,9:10,10:"jack",11:"queen",12:"king",13:"Ace"}

class Deck:
    def __init__(self):
        self.discards = []
        self.cards = []
        for s in ["S", "C", "H", "D"]:
            for r in range(1,14):
                self.cards.append(Card(s,r))
        random.shuffle(self.cards)

    def draw(self, n):
        cards = []
        for _ in range(n):
            cards.append(self.cards.pop())
        return cards
    
    def discard(self, card):
        self.discards.append(card)

    def shuffle(self):
        for _ in range(52):
            self.cards.append(self.discards.pop())
        random.shuffle(self.cards)

    def __str__(self):
        cards =""
        for card in self.cards:
            cards += (str(card.getRank()) + str(card.getSuit()) + "\n")
        return cards



deck = Deck()
