from pieces.piece import Piece
import math
from move import Move
from pieces.rook import Rook
from pieces.empty import Empty
from pieces.pawn import Pawn


class King(Piece):
    # Constructor defined in parents

    # defining the canMove method: involves defining how the piece moves
    def can_move(self, move, board):
        endR = move.end_row
        endC = move.end_col
        startR = self.row
        startC = self.col

        # general parameter check
        # uses distance formula to check if the move is legal
        if (endR == startR and endC == startC) or self.__pawn_check(endR, endC, board):
            return False

        distance = math.sqrt(math.pow(startR - endR, 2) + math.pow(startC - endC, 2))

        if ((distance == 1 or distance == math.sqrt(2)) and
                board.get_piece(endR, endC).color != self.color):
            return True
        elif (endR == 7 and endC == 6 and not self.hasMoved and
              (self.color == "white" and isinstance(board.get_piece(7, 7), Rook) and
               not board.get_piece(7, 7).hasMoved) and
              isinstance(board.get_piece(7, 6), Empty) and isinstance(board.get_piece(7, 5), Empty) and
              not self.vulnerable(7, 4, board) and not self.vulnerable(7, 5, board) and not self.vulnerable(7, 6, board) and
              not self.__pawn_check(7, 5, board)):
            board.castle("white king's side")
            return True
        elif (endR == 7 and endC == 2 and not self.hasMoved and
              (self.color == "white" and isinstance(board.get_piece(7, 0), Rook) and
               not board.get_piece(7, 0).hasMoved) and
              isinstance(board.get_piece(7, 1), Empty) and isinstance(board.get_piece(7, 2), Empty) and
              isinstance(board.get_piece(7, 3), Empty) and
              not self.vulnerable(7, 2, board) and not self.vulnerable(7, 3, board) and not self.vulnerable(7, 6, board) and 
              not self.__pawn_check(7, 3, board)):
            board.castle("white queen's side")
            return True
        elif (endR == 0 and endC == 6 and not self.hasMoved and
              (self.color == "black" and isinstance(board.get_piece(0, 7), Rook) and
               not board.get_piece(0, 7).hasMoved) and
              isinstance(board.get_piece(0, 6), Empty) and isinstance(board.get_piece(0, 5), Empty) and
              not self.vulnerable(0, 4, board) and not self.vulnerable(0, 5, board) and not self.vulnerable(0, 6, board) and 
              not self.__pawn_check(0, 5, board)):
            board.castle("black king's side")
            return True
        elif (endR == 0 and endC == 2 and not self.hasMoved and
              (self.color == "black" and isinstance(board.get_piece(0, 0), Rook) and
               not board.get_piece(0, 0).hasMoved) and
              isinstance(board.get_piece(0, 1), Empty) and isinstance(board.get_piece(0, 2), Empty) and
              isinstance(board.get_piece(0, 3), Empty) and
              not self.vulnerable(0, 2, board) and not self.vulnerable(0, 3, board) and not self.vulnerable(0, 6, board) and 
              not self.__pawn_check(0, 3, board)):
            board.castle("black queen's side")
            return True
        return False

    def __pawn_check(self, row, col, board):
        if self.color == "white":
            i = -1
        else: i = 1

        if (i == -1 and row <= 1) or (i == 1 and row >= 6):
            return False

        if col > 0:
            if(isinstance(board.get_piece(row + i, col - 1), Pawn) and 
                self.color != board.get_piece(row + i, col - 1).color):
                return True
        if col < 7:
            if(isinstance(board.get_piece(row + i, col + 1), Pawn) and 
                self.color != board.get_piece(row + i, col + 1).color):
                return True
        return False


    def __str__(self):
        return " K "
