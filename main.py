from chess import Chess
from gui import GUI

def main():
    gui = GUI()
    gui.gameLoop()

    # chess = Chess()
    # print(chess.board.__str__())

    # chess.game_loop()
    print("Program Complete")

if __name__=='__main__':
    main()
