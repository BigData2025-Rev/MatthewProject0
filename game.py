import json
from deck import Deck
from player import Player

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player(self.deck)
        self.round = 1
    def mode1(self):
        p = self.player
        p.addChips(500)
        payouts = {"high card":0,"pair":1,"two pair":3, "three of a kind": 5, "straight":10, "flush":15, "full house":20, "four of a kind": 50, "straight flush": 100}

        def contains_non_num(string):
            for s in str(string):
                if s not in [str(x) for x in range(10)]:
                    return True
            return False

        while self.round <= 5 and p.getChips() >= 0:
            print(f"Round {self.round} / 5")
            bet = ""
            while True:
                bet = input(f"How many chips will you bet? You have {p.getChips()}\n")
                if contains_non_num(bet):
                    print("Enter only numeric characters")
                    continue
                bet = int(bet)
                if bet > 5000:
                    print("Enter a value between 1 and 5000")
                    continue
                break
            
            p.addChips(-1*bet)
            p.draw(5)
            p.displayCards()
            discards = input("select cards to discard 1-5\n")
            for n in discards:
                if n in [str(x) for x in range(10)] and int(n) in range(1,6):
                    p.select(p.cards[int(n)-1])
            p.discard()
            p.displayCards()
            print(p.scoreHand()[0])
            winnings = bet * payouts[p.scoreHand()[0]]
            print(f"You win {winnings} chips")
            p.addChips(winnings)
            self.round +=1
            p.discardAll()
            self.deck.shuffle()
        print(f"Final score: {p.chips}")
        with open('scores.json', "r", encoding="utf-8") as f:
            scores = json.load(f)
        mode1Scores = scores["mode1"]
        mode1Scores.append(p.chips)
        mode1Scores.sort(reverse = True)
        if len(mode1Scores) > 10:
            mode1Scores.pop()
        with open('scores.json', "w", encoding="utf-8") as f:
            json.dump(scores, f)
        print("high scores:")
        for i in range(len(mode1Scores)):
            score = scores["mode1"][i]
            print(f"{i+1}. {score}")
            
game = Game()
game.mode1()