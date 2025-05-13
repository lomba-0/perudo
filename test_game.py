from game import Game, HumanPlayer
from advanced_players import ProbabilityPlayer

def main():
    # p = Player(1)
    # p.roll_dices()
    # print("Player 1 dices: ", [k.value for k in p.dices])
    
    debug = True

    p_0 = HumanPlayer(id=0)
    p_1 = ProbabilityPlayer(id=1)
    players = [p_0, p_1]
    game = Game(players=players, debug=debug)
    game.play()


if __name__ == "__main__":
    
    main()
