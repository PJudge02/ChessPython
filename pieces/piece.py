# abstraction
from abc import ABC, abstractmethod

from move import Move


class Piece(ABC):
    # constructor for abstract
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.hasMoved = False

    # takes in argument move (which has start and end position)
    # checks to see if the piece can move
    @abstractmethod
    def can_move(self, move, board):
        pass

    # when a piece has moved
    def moved(self) -> None:
        self.hasMoved = True

    # changes the row & col for the piece
    def piece_move(self, row, col):
        self.row = row
        self.col = col

    def vulnerable(self, row, col, board):
        move = Move()
        is_in_check = False
        checking = None
        pieces = board.black_pieces if self.color == "white" else board.white_pieces
        for piece in pieces:
            move.define_move(piece.row, piece.col, row, col)
            is_in_check = piece.can_move(move, board)
            if is_in_check:
                checking = piece
                break
        # print(board)
        return checking

    # toString method (is abstract)
    @abstractmethod
    def __str__(self):
        pass
