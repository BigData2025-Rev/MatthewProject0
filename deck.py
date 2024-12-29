import random
import json

class Card:
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank
        self.face = None

    def getRank(self):
        return self.rank
    def getSuit(self):
        return self.suit
    def __str__(self):
        return f"{self.rank}{self.suit} "
    def getActualRank(self):
        #the ace is highest, 2 is lowest
        return {1:"2",2:"3",3:"4",4:"5",5:"6",6:"7",7:"8",8:"9",9:"10",10:"jack",11:"queen",12:"king",13:"ace"}[self.rank]
    def setFace(self,face):
        self.face = face
        suit = {"S":"\u2660","H":"\u2665","D":"\u2666","C":"\u2663"}[self.suit]
        self.face = list(map(lambda s: s.replace("s",suit), self.face))
    def getFace(self):
        return self.face



class Deck:
    def __init__(self):
        self.discards = []
        self.cards = []
        for s in ["S", "C", "H", "D"]:
            for r in range(1,14):
                card = Card(r,s)
                self.cards.append(card)
                with open('cards.json', "r", encoding="utf-8") as f:
                    faces = json.load(f)
                card.setFace(faces[card.getActualRank()])
        random.shuffle(self.cards)

    def draw(self, n):
        cards = []
        for _ in range(n):
            cards.append(self.cards.pop())
            if len(self.cards) == 0:
                self.shuffle()
        return cards
    
    def discard(self, card):
        self.discards.append(card)

    def shuffle(self):
        #takes in the discard pile and shuffles 
        while len(self.discards) > 0:
            self.cards.append(self.discards.pop())
        random.shuffle(self.cards)

    def __str__(self):
        cards =""
        for card in self.cards:
            cards += (str(card.getRank()) + str(card.getSuit()) + "\n")
        return cards



