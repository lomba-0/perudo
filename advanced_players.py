from game import Player
import math
import random
    

class ProbabilityPlayer(Player):
    """
    A player that uses probability to make decisions.
    """
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.is_ai = True

    def bid(self, possible_bids, bid_history, tot_dices, debug=False):
        # Implement a probability-based decision-making algorithm
        i = 0
        probabilities = [] 
        for pb in possible_bids:

            prob = 0
            if pb == "D":
                bid = bid_history[-1]
                num = int(bid.split('-')[0])
                face = bid.split('-')[1]
                my_num = self.count(face)
                remaining_num = num - my_num
                remaining_tot = tot_dices - self.n_dices

                
                for i in range(remaining_num):
                    if face == "L":
                        prob += math.comb(remaining_tot, i) * ((1/6) ** i) * ((5/6) ** (remaining_tot - i))
                    else:
                        prob += math.comb(remaining_tot, i) * ((1/3) ** i) * ((2/3) ** (remaining_tot - i))
                
            else:
                num = int(pb.split('-')[0])
                face = pb.split('-')[1]
                my_num = self.count(face)

                remaining_num = num - my_num
                remaining_tot = tot_dices - self.n_dices

                # if debug:
                #     print(f"Player {self.id} - Remaining dices: {remaining_tot}, Remaining num: {remaining_num}, Face: {face}")

                if remaining_num <= 0:
                    prob = 1
                else:
                    prob = 0
                    for i in range(remaining_num, remaining_tot + 1):
                        if face == "L":
                            prob += math.comb(remaining_tot, i) * ((1/6) ** i) * ((5/6) ** (remaining_tot - i))
                        else:
                            prob += math.comb(remaining_tot, i) * ((1/3) ** i) * ((2/3) ** (remaining_tot - i))

                        # if debug:
                        #     print(f"N dices: {i} - Prob: {prob}, Remaining dices: {remaining_tot}, Remaining num: {remaining_num}, Face: {face}")

            probabilities.append(float(round(prob,3)))

        print(f"Probabilities: {probabilities}")
            
        # Choose the bid with the highest probability
        max_prob = max(probabilities)
        max_prob_indices = [i for i, prob in enumerate(probabilities) if prob == max_prob]
        max_prob_index = random.choice(max_prob_indices)
        
        return possible_bids[max_prob_index]
