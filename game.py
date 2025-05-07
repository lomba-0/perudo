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
        if self.value  == value or self.value == 1:
            return 1
        return 0
    
    def disp_value(self):
        if self.value == 1:
            return "L"
        else:
            return str(self.value)

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
        return np.sum([k.count(value) for k in self.dices])
    
    def loses(self):
        self.n_dices -= 1
        if self.n_dices == 0:
            self.alive = False
            print(f"Player {self.id} is out of the game")


class Game():

    def __init__(self, n_players=2, n_humans=1, n_dices=5, debug=False):
        self.debug = debug
        self.n_players = n_players
        self.n_alive = n_players
        self.n_humans = n_humans
        
        self.players = [Player(id = i, n_dices = n_dices) for i in range(n_players)]
        
        self.count_dices()

        for i in range(n_humans):
            self.players[i].is_ai = False

        self.playing_player = random.randint(0, n_players-1)

        self.current_bid = None
        self.previous_bid = None
        self.current_possible_bids = []
        self.bid_history = []

    def play(self):
        # Start the game
        print("==================================")
        print("Starting the game with ", self.n_players, " players")
        for i in range(self.n_humans):
            print("Player ", i, " is a human")
        # print("==================================")
        while self.n_alive > 1:
            # Roll dices for all players
            self.count_dices()
            self.roll_dices()

            if self.debug:
                for i in range(self.n_players):
                    print("Player ", i, " dices: ", [k.disp_value() for k in self.players[i].dices])
            else:
                for i in range(self.n_humans):
                    print("Player ", i, " dices: ", [k.disp_value() for k in self.players[i].dices])
            print("==================================")
            # Start the bidding phase
            while True:
                print("Player ", self.playing_player, " turn")
                self.play_turn()

                if self.current_bid == "D":
                    break

                if self.debug:
                    print("Current player: ", self.playing_player)
                    print("Next player: ", self.next_player())
                    print("Previous player: ", self.previous_player())
                    print("Current bid: ", self.current_bid)
                    print("Previous bid: ", self.previous_bid)
                    print("Bid history: ", self.bid_history)

                self.playing_player = self.next_player()
                # if self.debug:
                #     print("Current player: ", self.previous_player())
                #     print("Next player: ", self.playing_player)

            self.n_alive = len(self.whos_alive())
            self.bid_history = []
            self.current_bid = None
            self.previous_bid = None
            self.current_possible_bids = []
            print("+++++++++++ NEW ROUND +++++++++++")

            if self.debug:
                print("Alive players: ", self.whos_alive())
                
        print("==================================")
        print("Game Over")
        print("Player ", self.whos_alive()[0], " wins")
        print("==================================")

    def play_turn(self):

        self.previous_bid = self.current_bid
        self.possible_bids()

        if self.players[self.playing_player].is_ai:
            self.ai_bid()
        else:
            self.human_bid()

        if self.current_bid == "D":
            print(f"Player {self.playing_player} dares")
            self.dare()
        else:
            self.bid_history.append(self.current_bid)
            print(f"Player {self.playing_player} bids {self.current_bid}")
            print("--------------------------------")


    def human_bid(self):
        while True:
            bid = input("Enter your bid: ")
            if bid in self.current_possible_bids:
                break
            else:
                print("Invalid bid. Try again.")

        self.current_bid = bid

       
    def ai_bid(self):
        # AI logic to make a bid
        # For now, we will just randomly select a bid from the possible bids
        bid = random.choice(self.current_possible_bids)
        self.current_bid = bid

    def dare(self):
        # Check if the player who made the bid has lost
        if self.is_last_bid_correct():
            print(f"Player {self.playing_player} loses a dice!")
            self.players[self.playing_player].loses()
        else:
            print(f"Player {self.previous_player()} loses a dice!")
            self.players[self.previous_player()].loses()
            self.playing_player = self.previous_player()

    def is_last_bid_correct(self):
        num_dices = int(self.previous_bid.split('-')[0])
        dice_face = self.previous_bid.split('-')[1]

        num = np.sum([k.count(dice_face) for k in self.players])

        if num >= num_dices:
            return True
        else:
            return False


    def possible_bids(self):
        
        bids = []

        if self.current_bid is None:
            for j in range(2, 7):
                bids.append(f"1-{j}")

        else:

            num_dices = int(self.current_bid.split('-')[0])
            dice_face = self.current_bid.split('-')[1]
            
            if dice_face == "L":
                if num_dices + 1 <= self.tot_dices:
                    bids.append(f"{num_dices+1}-L")
                if num_dices + 2 <= self.tot_dices:
                    bids.append(f"{num_dices+2}-L")

                min_num = int(2 * num_dices)
                if min_num <= self.tot_dices:
                    for j in range(2, 7):
                        bids.append(f"{min_num}-{j}")
                        
            else:
                min_lama = int(np.floor(num_dices / 2 + 1))
                dice_face = int(dice_face)
                for j in range(dice_face+1, 7):
                    bids.append(f"{num_dices}-{j}")
                if num_dices + 1 <= self.tot_dices:
                    for j in range(2, 7):
                        bids.append(f"{num_dices+1}-{j}")
                bids.append(f"{min_lama}-L")
                bids.append(f"{min_lama+1}-L")
            bids.append("D")

        self.current_possible_bids = bids

        print("Possible bids: ", bids)
            
    def whos_alive(self):
        return [i for i in range(self.n_players) if self.players[i].alive]

    def roll_dices(self):
        for i in range(self.n_players):
            if self.players[i].alive:
                self.players[i].roll_dices()

    def next_player(self):
        current_player = self.playing_player
        while True:
            next_player = (current_player + 1) % self.n_players
            if self.players[next_player].alive == True:
                return next_player
            current_player = next_player

    def previous_player(self):
        current_player = self.playing_player
        while True:
            next_player = (current_player - 1) % self.n_players
            if self.players[next_player].alive == True:
                return next_player
            current_player = next_player

    def count_dices(self):
        self.tot_dices = np.sum([k.n_dices for k in self.players if k.alive])
