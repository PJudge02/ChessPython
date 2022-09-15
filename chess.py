# Move
from move import Move
# Board
from board import Board, Result
# colored text for console output
from colorama import Fore, Style
# pieces
from pieces.pawn import Pawn
from pieces.knight import Knight
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.queen import Queen


# GUI


class Chess:
    # Chess constructor
    def __init__(self):
        self.board = Board()
        self.move = Move()
        self.whiteToMove = True

    # presents the user with a list of pieces to choose from
    def promote_pawn(self, piece: Pawn) -> None:
        print("1. Queen")
        print("2. Rook")
        print("3. Bishop")
        print("4. Knight")
        choice = input("Please choose a piece to promote to: ").strip()
        match choice:
            case "1":
                self.board.board[piece.row][piece.col] = Queen(piece.row, piece.col, piece.color)
            case "2":
                self.board.board[piece.row][piece.col] = Rook(piece.row, piece.col, piece.color)
            case "3":
                self.board.board[piece.row][piece.col] = Bishop(piece.row, piece.col, piece.color)
            case "4":
                self.board.board[piece.row][piece.col] = Knight(piece.row, piece.col, piece.color)
            case _:
                print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
                self.promote_pawn(piece)

    # the main loop where the game happens
    def game_loop(self) -> None:
        # loop represents the overall game loop
        while True:  # input("Would you like to move? (y/n)\n") == "y"

            # GET USER INPUT--------------------------------------------------------------------

            move_input = input("Please input your move with the following notation: " +
                               "[pieceLocation]-[pieceDestination] (Example: a2-a3)\n").strip().lower()

            if self.move.set_move(move_input) is False:
                print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
                continue

            piece = self.board.get_piece(self.move.start_row, self.move.start_col)

            # CHECK USER INPUT IS VALID----------------------------------------------------------
            # check if the piece is the player's color
            if (self.whiteToMove and piece.color == "black") or (self.whiteToMove is False and piece.color == "white"):
                print(Fore.RED + "Wrong Color!" + Style.RESET_ALL)
                continue

            # MAKE THE "MOVE" CHANGE------------------------------------------------------------
            result = self.board.move_piece(self.move, self.whiteToMove)

            match result:
                # if the move was successful
                case Result.OK:
                    self.whiteToMove = not self.whiteToMove
                    # print(self.board.__str__())
                case Result.ILLEGAL:
                    print(Fore.RED + "That was an invalid move, please make a legal move" + Style.RESET_ALL)
                case Result.CHECK:
                    print(Fore.RED + "King is in Check!" + Style.RESET_ALL)
                case Result.PROMOTE:
                    self.promote_pawn(piece)
                    self.whiteToMove = not self.whiteToMove
                    # print(self.board.__str__())
                case Result.CHECKMATE:
                    print(Fore.RED + "Checkmate! " + "White wins!" if self.whiteToMove else "Black wins!" + Style.RESET_ALL)
                    break
