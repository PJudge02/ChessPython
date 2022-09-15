from pieces.piece import Piece


class Empty(Piece):
    # Constructor defined in parents
    # def __init__(self, xpos, ypos, color):
    #     p.__init__(self, xpos, ypos, color)

    # can't move
    def can_move(self, move, board):
        # print("This space is Empty")
        return False

    # toString function
    def __str__(self):
        return "   "

    def name(self):
        return "empty"
