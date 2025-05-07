from game import *


def main():
    # p = Player(1)
    # p.roll_dices()
    # print("Player 1 dices: ", [k.value for k in p.dices])
    
    debug = False
    

    game = Game(n_players=2, n_humans=1, n_dices=5, debug=debug)
    game.play()


if __name__ == "__main__":
    
    main()
