import json
import sys
import msvcrt
import random
from deck import Deck
from player import Player, Cpu

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player(self.deck)
        self.round = 1

    def selectMode(self):
        self.clearScreen()
        while True:
            print("Select a game mode:\n 1) single player     2) 4 player\n")
            selection = str(msvcrt.getwche())
            if selection not in ["1","2"]:
                print("input 1 or 2 to select mode")
                continue
            elif selection == "1":
                self.mode1()
                break
            else:
                self.mode2()
                break

    def clearScreen(self):
        print("\033c")
    def waitForInput(self):
        print("Press any key to draw")
        msvcrt.getch()

    def contains_non_num(self,string):
        for s in str(string):
            if s not in [str(x) for x in range(10)]:
                return True
        return False
    def end_of_game(self, gameMode, score):
        print(f"Final score: {score}")

        #update score file
        with open('scores.json', "r", encoding="utf-8") as f:
            scores = json.load(f)
        mode1Scores = scores[gameMode]
        mode1Scores.append(score)
        mode1Scores.sort(reverse = True)
        if len(mode1Scores) > 10:
            mode1Scores.pop()
        with open('scores.json', "w", encoding="utf-8") as f:
            json.dump(scores, f)
        print("high scores:")

        for i in range(len(mode1Scores)):
            score = scores[gameMode][i]
            print(f"{i+1}. {score}")
        while True:
            print("1) Play again    2) Change mode    3) Quit")
            selection = str(msvcrt.getwche())
            if selection not in ("1", "2", "3"):
                print("Press 1, 2, or 3")
                continue
            if selection == "1":
                mode = self.mode1 if game == "mode1" else self.mode2
                mode()
                break
            elif selection == "2":
                self.selectMode()
            elif selection == "3":
                self.clearScreen()
                sys.exit(0)
    def mode1(self):
        p = self.player
        p.setChips(500)
        self.round = 1
        payouts = {"high card":0,"pair":1,"two pair":3, "three of a kind": 5, "straight":10,
                    "flush":15, "full house":20, "four of a kind": 50, "straight flush": 100}

        #Game loop
        while self.round <= 5 and p.getChips() >= 0:
            p.discardAll()
            self.deck.shuffle()
            self.clearScreen()
            print(f"Round {self.round} / 5")
            bet = ""
            while True:
                bet = input(f"How many chips will you bet? You have {p.getChips()}\n")
                if self.contains_non_num(bet):
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
            discards = input("select cards to discard (1-5) or press enter to continue\n")

            for n in set(discards):
                if n in [str(x) for x in range(10)] and int(n) in range(1,6):
                    p.select(p.cards[int(n)-1])

            p.discard()
            p.displayCards()
            print(p.scoreHand()[0])
            winnings = bet * payouts[p.scoreHand()[0]]
            print(f"You win {winnings} chips\nPress any key to continue")
            p.addChips(winnings)
            print()
            self.round +=1
            msvcrt.getch()
        self.clearScreen()
        self.end_of_game("mode1",p.getChips())

    def mode2(self):
        self.round = 1
        p = self.player
        p.setChips(500)
        cpu1 = Cpu(self.deck,500)
        cpu2 = Cpu(self.deck,500)
        cpu3 = Cpu(self.deck,500)
        smallblind = 25
        bigblind = 2 * smallblind
        players = [self.player,cpu1,cpu2,cpu3]
        startingPos = random.randrange(0,4)
        order = ["high card","pair","two pair", "three of a kind", "straight",
                    "flush", "full house", "four of a kind", "straight flush"]
        
        while self.round <= 5 and p.getChips() >= 0:
            print(f"\nround {self.round}/5")
            playersOut = []
            self.deck.shuffle()
            pot = 0
            turn = 0
            bet = bigblind
            #go through each player from the random starting position
            for player in [players[(x+startingPos) % 4] for x in range(4)]:
                player.draw(5)
                print("\n")
                player.setIsOut(False)
                if player is p:
                    if turn == 0:
                        self.waitForInput()
                        p.displayCards()
                        print(f"You post the small blind of {smallblind} chips")
                        p.addChips(-1*smallblind)
                        pot += smallblind
                        turn += 1
                    elif turn == 1:
                        self.waitForInput()
                        p.displayCards()
                        print(f"You post the big blind of {bigblind} chips")
                        p.addChips(-1*bigblind)
                        pot += bigblind
                        turn += 1
                    else:
                        self.waitForInput()
                        p.displayCards()
                        while True:
                            print(f"1) fold    2) call    3) raise\n You have {p.getChips()} chips and the bet is {bet} chips")
                            selection = str(msvcrt.getwche())
                            if selection not in ("1", "2", "3"):
                                print("Press 1, 2, or 3")
                                continue
                            if selection == "1":
                                print("You fold")
                                p.setIsOut(True)
                                playersOut.append(player)
                                break
                            elif selection == "2":
                                pot += bet
                                p.addChips(-1*bet)
                                print(f"You bet {bet} chips")
                                break
                            elif selection == "3":
                                bet += bigblind
                                pot += bet
                                p.addChips(-1*bet)
                                print(f"You bet {bet} chips")
                                break
                else:
                    if turn == 0:
                        print(f"player {players.index(player)} posts the small blind of {smallblind} chips")
                        player.addChips(-1*smallblind)
                        pot += smallblind
                        turn += 1
                    elif turn == 1:
                        print(f"player {players.index(player)} posts the big blind of {bigblind} chips")
                        player.addChips(-1*smallblind)
                        pot += smallblind
                        turn += 1
                    else:
                        action = player.bet()
                        if action == "fold":
                            print(f"player {players.index(player)} folds")
                            playersOut.append(player)
                            player.setIsOut(True)
                        elif action == "call":
                            pot += bet
                            player.addChips(-1*bet)
                            print(f"player {players.index(player)} calls")
                        elif action == "raise":
                            bet += bigblind
                            pot += bet
                            player.addChips(-1*bet)
                            print(f"player {players.index(player)} raises")
            #Draw round
            #for player in [players[(x+startingPos) % 4] for x in range(4)]:
            for player in players:
                if len(playersOut) == 3:
                    break
                if not player.getIsOut():
                    print("\n")
                    if player is p:
                        discards = input("select cards to discard (1-5) or press enter to continue\n")
                        for n in set(discards):
                            if n in [str(x) for x in range(10)] and int(n) in range(1,6):
                                p.select(p.cards[int(n)-1])
                        p.discard()
                        p.displayCards()

                        while True:
                            print(f"1) fold    2) call    3) raise\n You have {p.getChips()} chips and the bet is {bet} chips")
                            selection = str(msvcrt.getwche())
                            if selection not in ("1", "2", "3"):
                                print("Press 1, 2, or 3")
                                continue
                            if selection == "1":
                                print("You fold")
                                p.setIsOut(True)
                                playersOut.append(player)
                                break
                            elif selection == "2":
                                pot += bet
                                p.addChips(-1*bet)
                                print(f"You bet {bet} chips")
                                break
                            elif selection == "3":
                                bet += bigblind
                                pot += bet
                                p.addChips(-1*bet)
                                print(f"You bet {bet} chips")
                                break
                    else:
                        player.discard()
                        action = player.bet()
                        if action == "fold":
                            print(f"player {players.index(player)} folds")
                            playersOut.append(player)
                            player.setIsOut(True)
                        elif action == "call":
                            pot += bet
                            player.addChips(-1*bet)
                            print(f"player {players.index(player)} calls")
                        elif action == "raise":
                            bet += bigblind
                            pot += bet
                            player.addChips(-1*bet)
                            print(f"player {players.index(player)} raises")

            highestHand = 0
            tieBreaker = 0
            winning = 0
            for player in players:
                if not player.getIsOut():
                    strength = order.index(player.scoreHand()[0])
                    if  strength > highestHand or (strength == highestHand and player.scoreHand()[1]>tieBreaker):
                        highestHand = strength
                        winning = players.index(player)
                        tieBreaker = player.scoreHand()[1]
            if winning == 0:
                print(f"You won the pot of {pot} chips!")
                p.addChips(pot)
            else:
                hand = players[winning].scoreHand()
                rank = {1:"2",2:"3",3:"4",4:"5",5:"6",6:"7",7:"8",8:"9",
                        9:"10",10:"jack",11:"queen",12:"king",13:"ace"}[tieBreaker]
                print(f"player {winning} wins with a {hand[0]}, {rank} high")
                players[winning].addChips(pot)
            self.round += 1
            for player in players:
                player.discardAll()
            startingPos += 1
        self.end_of_game("mode2",p.getChips())




game = Game()
game.selectMode()
