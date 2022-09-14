from pieces.piece import Piece
from pieces.empty import Empty


class Rook(Piece):
    # Constructor defined in parents

    # defining the canMove method: involves defining how the piece moves
    def can_move(self, move, board):
        endR = move.end_row
        endC = move.end_col
        startR = move.start_row
        startC = move.start_col
        # general parameter check
        if ((endR == startR and endC == startC) or
                (startR != endR and startC != endC)):
            return False

        # checks horizontal or vertical
        # then checks to make sure there are no pieces in the way & the end square is the right color
        HORIZONTAL = 0
        VERTICAL = 0
        if startC == endC:
            VERTICAL = (startR - endR) / abs(endR - startR)
        else:
            HORIZONTAL = (endC - startC) / abs(endC - startC)
        for diff in range(1, abs(startR - endR) + abs(startC - endC)):
            if not isinstance(board.get_piece(int(startR - diff * VERTICAL), int(startC + diff * HORIZONTAL)), Empty):
                return False
        if board.get_piece(endR, endC).color == self.color:
            return False
        return True


    def __str__(self):
        return " R "
