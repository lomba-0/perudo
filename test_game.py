from game import *


def main():
    p = Player(1)
    p.roll_dices()
    print("Player 1 dices: ", [k.value for k in p.dices])


    
if __name__ == "__main__":
    
    main()
