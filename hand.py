from deck import Deck, Card

class Hand:
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

    def score(self):
        ranks = [c.getRank() for c in self.cards]
        suits = [c.getSuit() for c in self.cards]

        if suits.count(suits[0]) == 5:
            if ranks == [1,2,3,4,13]:
                return "straight flush"
            for i in range(5):
                if ranks[i] != ranks[i+1] + 1:
                    return "flush"
                return "straight flush"
        
        for i in range(5):
            if ranks[i] != ranks[i+1] + 1:
                break
            if i == 4:
                return "straight"
            
        if ranks == [1,2,3,4,13]:
            return "straight"
        
        counts = []
        for r in ranks:
            count = ranks.count(r)
            counts.append(count)
        for r in ranks:
            if 4 in counts:
                return "four of a kind"
            elif 3 in counts:
                if 2 in counts:
                    return "full house"
                else: return "three of a kind"
            elif 2 in counts:
                if counts.count(2) > 2:
                    return "two pair"
                else: return "pair"
        return "high card"

hand = Hand(Deck())
hand.draw(5)
print([str(s) for s in hand.cards])
print(hand.score())