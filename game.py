import random
import re
import numpy as np

class Dice():
    def __init__(self):
        self.roll()

    def roll(self):
        self.value = random.randint(1, 6)
        return self.value

    def count(self, value):
        if self.value  == value | self.value == 1:
            return 1
        return 0
    
    def disp(self):
        if self.value == 1:
            print("L")
        else:
            print(self.value)

class Player():
    def __init__(self, id, n_dices = 5, is_ai=True):
        self.id = id
        self.n_dices = n_dices
        self.dices = []
        self.is_ai = is_ai
        self.alive = True

    def roll_dices(self):
        self.dices = [Dice() for i in range(self.n_dices)]
        return self.dices

    def count(self, value):
        return [k.count(value) for k in self.dices].sum()
    
    def loses(self):
        self.n_dices -= 1
        if self.n_dices == 0:
            self.alive = False


class Game():

    n_players = 2

    def __init__(self, n_players=2, n_humans=1, n_dices=5):
        self.n_players = n_players
        self.n_alive = n_players
        self.n_humans = n_humans
        
        self.players = [Player(id = i, n_dices = n_dices) for i in range(n_players)]

        for i in range(n_humans):
            self.players[i].is_ai = False

        self.playing_player = random.randint(0, 5)

        self.current_bid = None
        self.current_possible_bids = []
        self.bid_history = []

    def play(self):
        while self.n_alive > 1:
            
            self.playing_player = (self.playing_player + 1) % self.n_players
            if not self.players[self.playing_player].alive:
                continue
            print("Player ", self.playing_player, " turn")

            self.play_turn()

    def play_turn(self):

        self.possible_bids()


    def possible_bids(self):
        
        num_dices = self.current_bid[0]
        dice_face = self.current_bid[1]
        bids = []

        if dice_face == "L":
            bids.append(f"{num_dices+1}-L")
            bids.append(f"{num_dices+2}-L")

            min_num = 2 * num_dices
            for j in range(1, 7):
                bids.append(f"{min_num}-{j}")
        else:
            min_lama = np.floor(num_dices / 2 + 1)
            dice_face = int(dice_face)
            for j in range(dice_face+1, 7):
                bids.append(f"{num_dices}-{j}")
            for j in range(1, 7):
                bids.append(f"{num_dices}-{j}")
            bids.append(f"{min_lama}-L")
            bids.append(f"{min_lama+1}-L")

        bids.append("D")
        self.current_possible_bids = bids

        print("Possible bids: ", bids)
            

