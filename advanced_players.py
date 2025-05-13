from game import Player
import math
    

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

            if pb == "D":
                bid = bid_history[-1]
                num = int(bid.split('-')[0])
                face = bid.split('-')[1]
                my_num = self.count(face)
                remaining_num = num - my_num
                remaining_tot = tot_dices - self.n_dices

                prob = 0
                for i in range(remaining_num, remaining_tot + 1):
                    if face == "L":
                        prob += math.comb(remaining_tot, i) * ((1/6) ** i) * ((5/6) ** (remaining_tot - i))
                    else:
                        prob += math.comb(remaining_tot, i) * ((1/3) ** i) * ((2/3) ** (remaining_tot - i))

                probabilities.append(float(round(1-prob,3)))

                
            else:
                num = int(pb.split('-')[0])
                face = pb.split('-')[1]
                my_num = self.count(face)
                remaining_num = num - my_num
                remaining_tot = tot_dices - self.n_dices

                prob = 0
                for i in range(remaining_num):
                    if face == "L":
                        prob += math.comb(remaining_tot, i) * ((1/6) ** i) * ((5/6) ** (remaining_tot - i))
                    else:
                        prob += math.comb(remaining_tot, i) * ((1/3) ** i) * ((2/3) ** (remaining_tot - i))

                probabilities.append(float(round(prob,3)))

        # if debug:
        # print(f"Possible bids: {possible_bids}")
        print(f"Probabilities: {probabilities}")
            
        # Choose the bid with the highest probability
        max_prob = max(probabilities)
        max_prob_index = probabilities.index(max_prob)
        return possible_bids[max_prob_index]
            