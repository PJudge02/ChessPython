import enum
from operator import indexOf
from string import whitespace
from tabnanny import check
from colorama import Fore, Style
from pieces.empty import Empty
from pieces.pawn import Pawn
from pieces.knight import Knight
from pieces.piece import Piece
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.king import King
from move import Move


class Result(enum.IntEnum):
    """
    Enum for move results
    """
    OK = 0
    ILLEGAL = 1
    CHECK = 2
    PROMOTE = 3
    CHECKMATE = 4
    STALEMATE = 5


class Board:
    def __init__(self):
        self.white_pieces = []
        self.black_pieces = []
        self.board = []
        self.create_board()
        self.empty = Empty(-1, -1, "n/a")
        self.en_passant = []
        self.past_piece = None
        self.old_move = Move()
        self.removal_piece_index = -1

    def create_board(self):
        self.board = [[Empty(-1, -1, "n/a") for col in range(8)] for row in range(8)]

        self.white_pieces.append(Rook(7, 0, "white"))
        self.white_pieces.append(Knight(7, 1, "white"))
        self.white_pieces.append(Bishop(7, 2, "white"))
        self.white_pieces.append(Queen(7, 3, "white"))
        self.white_pieces.append(King(7, 4, "white"))
        self.white_pieces.append(Bishop(7, 5, "white"))
        self.white_pieces.append(Knight(7, 6, "white"))
        self.white_pieces.append(Rook(7, 7, "white"))
        for i in range(8):
            self.white_pieces.append(Pawn(6, i, "white"))

        for p in self.white_pieces:
            self.board[p.row][p.col] = p

        self.black_pieces.append(Rook(0, 0, "black"))
        self.black_pieces.append(Knight(0, 1, "black"))
        self.black_pieces.append(Bishop(0, 2, "black"))
        self.black_pieces.append(Queen(0, 3, "black"))
        self.black_pieces.append(King(0, 4, "black"))
        self.black_pieces.append(Bishop(0, 5, "black"))
        self.black_pieces.append(Knight(0, 6, "black"))
        self.black_pieces.append(Rook(0, 7, "black"))
        for i in range(8):
            self.black_pieces.append(Pawn(1, i, "black"))

        for p in self.black_pieces:
            self.board[p.row][p.col] = p

    # returns the piece at a specific location 
    def get_piece(self, row, col) -> Piece:
        return self.board[row][col]

    # determine if the player's king is in check
    def in_check(self, white_turn):
        king = self.white_pieces[4] if white_turn else self.black_pieces[4]
        # print(f"{king.row} row & {king.col} col & {king.color} color")
        return king.vulnerable(king.row, king.col, self)
    
    # determines if the game is a stalemate
    def in_stalemate(self, white_turn):
        checking_piece = self.in_check(white_turn)
        if(not checking_piece):
            for row in range(8):
                for col in range(8):
                    for p in self.white_pieces if white_turn else self.black_pieces:
                        if (p.can_move(Move(p.row, p.col, row, col), self) and 
                            (isinstance(p, King) and not p.vulnerable(row, col, self))):
                            print(f'{p} {p.row},{p.col}')
                            return False
        else: 
            return False
        return True

    def in_checkmate(self, white_turn):
        checking_piece = self.in_check(white_turn)
        if checking_piece:
            king = self.white_pieces[4] if white_turn else self.black_pieces[4]
            # check if the king can move to a square that is not in check
            for i in range(-1, 1):
                for j in range(-1, 1):
                    if i == 0 and j == 0:
                        continue
                    if king.row + i < 0 or king.row + i > 7 or king.col + j < 0 or king.col + j > 7:
                        continue
                    if (king.can_move(Move(king.row, king.col, king.row + i, king.col + j), self)
                        and not king.vulnerable(king.row + i, king.col + j, self)):
                        print(f'king can move to {king.row + i},{king.col + j}')
                        return False
            # check if the player can take the piece checking the king
            for p in self.white_pieces if white_turn else self.black_pieces:
                if p.can_move(Move(p.row, p.col, checking_piece.row, checking_piece.col), self):
                    print(f'{p} {p.row},{p.col}')
                    return False
                if not isinstance(checking_piece, Knight) and not isinstance(p, King):
                    if king.row == checking_piece.row:
                        for c in range(1, abs(king.col - checking_piece.col)):
                            if p.can_move(Move(p.row, p.col, king.row,
                                               king.col + c * (1 if king.col < checking_piece.col else -1)), self):
                                print(f'{p} {p.row},{p.col}')
                                return False
                    elif king.col == checking_piece.col:
                        for r in range(1, abs(king.row - checking_piece.row)):
                            if p.can_move(
                                    Move(p.row, p.col, king.row + r * (1 if king.row < checking_piece.row else -1),
                                         king.col), self):
                                print(f'{p} {p.row},{p.col}')
                                return False
                    else:
                        for r in range(1, abs(king.row - checking_piece.row)):
                            for c in range(1, abs(king.col - checking_piece.col)):
                                if r == c and p.can_move(
                                        Move(p.row, p.col, king.row + r * (1 if king.row < checking_piece.row else -1),
                                             king.col + c * (1 if king.col < checking_piece.col else -1)), self):
                                    print(f'{p} {p.row},{p.col}')
                                    print(f"piece is {p}")
                                    return False
            return True
        return False

    # moves a piece to the end location and sets the old square empty
    def move_piece(self, move, white_turn):
        if not self.board[move.start_row][move.start_col].can_move(move, self):
            return Result.ILLEGAL
        self.set_undo(move)
        if len(self.en_passant) != 0:
            if self.board[move.start_row][move.start_col].color == "white":
                self.board[move.end_row + 1][move.end_col] = self.empty
            else:
                self.board[move.end_row - 1][move.end_col] = self.empty

        self.board[move.start_row][move.start_col].piece_move(move.end_row, move.end_col)#---------------
        self.board[move.end_row][move.end_col] = self.board[move.start_row][move.start_col]
        self.board[move.start_row][move.start_col] = self.empty

        # moving into check
        if self.in_check(white_turn):
            # print("HELLO---------------------")
            self.undo()
            # print("")
            return Result.CHECK

        if len(self.en_passant) != 0:
            if (white_turn and self.en_passant[0].color == "white") \
                    or (not white_turn and self.en_passant[0].color == "black"):
                self.en_passant.clear()

        # pawn promotion
        if isinstance(self.get_piece(move.end_row, move.end_col), Pawn) and \
                ((white_turn and move.end_row == 0) or (not white_turn and move.end_row == 7)):
            return Result.PROMOTE

        # checkmate (check the pieces of the other player)
        if self.in_checkmate(not white_turn):
            return Result.CHECKMATE

        return 0

    # when castling is happening
    def castle(self, castle_loc):
        if castle_loc == "white king's side":
            self.board[7][5] = self.board[7][7]
            self.board[7][7] = self.empty
        elif castle_loc == "white queen's side":
            self.board[7][3] = self.board[7][0]
            self.board[7][0] = self.empty
        elif castle_loc == "black king's side":
            self.board[0][5] = self.board[0][7]
            self.board[0][7] = self.empty
        elif castle_loc == "black queen's side":
            self.board[0][3] = self.board[0][0]
            self.board[0][0] = self.empty

    # handles promoting a piece
    def pawn_promotion(self, color, piece, newPiece):
        if (color == "white"):
            arr = self.white_pieces
        else:
            arr = self.black_pieces
        position = arr.index(piece)
        arr[position] = newPiece
        self.board[piece.row][piece.col] = newPiece

        # for pieces in arr:
        #     print(pieces)

        

    # sets pieces and squares in case undo is needed
    def set_undo(self, move):
        self.old_move.define_move(move.start_row, move.start_col, move.end_row, move.end_col)
        self.past_piece = self.board[move.end_row][move.end_col]
        # print(f"Past piece is {self.past_piece}")
        if(self.past_piece.color == "black"):
            self.removal_piece_index = self.black_pieces.index(self.board[move.end_row][move.end_col])
            self.black_pieces[self.removal_piece_index] = (
                Empty(move.end_row, move.end_col,"black")
            )
        elif(self.past_piece.color == "white"):
            self.removal_piece_index = self.white_pieces.index(self.board[move.end_row][move.end_col])
            self.white_pieces[self.removal_piece_index] = (
                Empty(move.end_row, move.end_col,"white")
            )
            # for i in self.white_pieces:
            #     print(i)


    # if a move wasn't legal (leaving the king in check) then
    def undo(self):
        if len(self.en_passant) != 0:
            if self.past_piece.color == "white":
                self.board[self.old_move.end_row + 1][self.old_move.end_col] = self.past_piece
            else:
                self.board[self.old_move.end_row - 1][self.old_move.end_col] = self.past_piece
        else:

            self.board[self.old_move.start_row][self.old_move.start_col] = self.board[self.old_move.end_row][
                self.old_move.end_col]
            self.board[self.old_move.end_row][self.old_move.end_col] = self.past_piece
            # print(f"Comparing the square you were moving into and the square you were at is: {self.board[self.old_move.end_row][self.old_move.end_col] == self.board[self.old_move.start_row][self.old_move.start_col]}")
        if self.past_piece.color == "white":
            self.white_pieces[self.removal_piece_index] = self.past_piece
        elif self.past_piece.color == "black":
             self.black_pieces[self.removal_piece_index] = self.past_piece
        

    def __str__(self):
        print_string = "Chess Board: \n"
        # gets the row in board
        for rowArr in self.board:
            for pieceIndex in range(8):
                # sets the color for the pieces
                if rowArr[pieceIndex].color == "black":
                    print_string += Fore.RED
                elif rowArr[pieceIndex].color == "white":
                    print_string += Fore.BLUE
                print_string += f"{str(rowArr[pieceIndex])}"
                print_string += Style.RESET_ALL
                if pieceIndex != 7:
                    print_string += "|"
            if self.board[7] != rowArr:
                print_string += "\n___ ___ ___ ___ ___ ___ ___ ___\n"
        return print_string
