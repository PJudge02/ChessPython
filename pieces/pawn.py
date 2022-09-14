from pieces.piece import Piece
from pieces.empty import Empty


class Pawn(Piece):
    # Constructor defined in parents
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.en_passant = 0  # 1 - take left, 2 - take right (objective view)

    # checks and activates opponents pawn en passant if possible
    def en_passant_move(self, end_r, end_c, board):
        edge_right = 1
        edge_left = 1
        if end_c == 7:
            edge_right = 0
        if end_c == 0:
            edge_left = 0
        if (isinstance(board.get_piece(end_r, end_c + 1 * edge_right), Pawn) and
                isinstance(board.get_piece(end_r, end_c - 1 * edge_left), Pawn) and
                board.get_piece(end_r, end_c + 1 * edge_right).color != self.color and
                board.get_piece(end_r, end_c - 1 * edge_right).color != self.color):
            board.get_piece(end_r, end_c + 1 * edge_right).en_passant = 1
            board.get_piece(end_r, end_c - 1 * edge_right).en_passant = 2
            board.en_passant.append(board.get_piece(end_r, end_c + 1 * edge_right))
            board.en_passant.append(board.get_piece(end_r, end_c - 1 * edge_right))
        elif (isinstance(board.get_piece(end_r, end_c + 1 * edge_right), Pawn) and
              board.get_piece(end_r, end_c + 1 * edge_right).color != self.color):
            board.get_piece(end_r, end_c + 1 * edge_right).en_passant = 1
            board.en_passant.append(board.get_piece(end_r, end_c + 1 * edge_right))
        elif (isinstance(board.get_piece(end_r, end_c - 1 * edge_right), Pawn) and
              board.get_piece(end_r, end_c - 1 * edge_right).color != self.color):
            board.get_piece(end_r, end_c - 1 * edge_right).en_passant = 2
            board.en_passant.append(board.get_piece(end_r, end_c - 1 * edge_right))

    # defining the canMove method: involves defining how the piece moves
    def can_move(self, move, board):
        endR = move.end_row
        endC = move.end_col
        startR = move.start_row
        startC = move.start_col
        color = self.color

        # up-2, up1, take diagnol, en passant, false
        if (
                isinstance(board.get_piece(endR, endC), Empty) and
                self.hasMoved is False and
                startC == endC and
                ((color == "white" and endR == 4) or (color == "black" and endR == 3))
        ):
            self.en_passant_move(endR, endC, board)
            return True
        elif (
                isinstance(board.get_piece(endR, endC), Empty) and startC == endC and
                ((color == "white" and endR ==  startR - 1) or (color == "black" and endR ==  startR + 1))):
            return True
        elif (
                board.get_piece(endR, endC).color != "n/a" and
                board.get_piece(endR, endC).color != color and
                (startC + 1 == endC or startC - 1 == endC) and
                ((color == "white" and endR ==  startR - 1) or
                 (color == "black" and endR ==  startR + 1))
        ):
            return True
        elif (
                (self.en_passant == 1 and endC == startC- 1) or
                (self.en_passant == 2 and endC == startC + 1) and
                ((color == "white" and endR ==  startR - 1) or (color == "black" and endR ==  startR + 1))
        ):
            return True
        return False

    def __str__(self):
        return " P "
