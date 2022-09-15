from pieces.piece import Piece
import math


class Knight(Piece):
    # Constructor defined in parents

    # defining the canMove method: involves defining how the piece moves
    def can_move(self, move, board):
        endR = move.end_row
        endC = move.end_col
        startR = move.start_row
        startC = move.start_col

        # general parameter check
        # uses distance formula to check if the move is legal
        if endR == startR and endC == startC:
            # print("HERE")
            return False

        if (math.sqrt(math.pow(startR - endR, 2) + math.pow(startC - endC, 2)) != math.sqrt(5) or
                board.get_piece(endR, endC).color == self.color):
            # print("HERE!")
            return False

        return True

    def __str__(self):
        return "Kn "

    def name(self):
        return "knight"
