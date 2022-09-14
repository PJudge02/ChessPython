from turtle import reset
import pygame
from board import Board, Result
from move import Move
from svg_handler import SVG_Handler as svgh

# colored text for console output
from colorama import Fore, Style
# pieces
from pieces.pawn import Pawn
from pieces.knight import Knight
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.king import King
from pieces.empty import Empty

import math

# pawn promotion
from pawn_promotion import pawn_promotion as pp

WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Chess")

SQUARE_SIZE = 75
PIECE_SCALING = 1.7

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (150, 75, 0)
GREEN = (0, 255, 0)

SQUARE_SEL = [-1, -1]
MOUSE_CLICKED = False

# PIECE = pygame.image.load('ChessPython/images/pieces/black_bishop.svg')
# BLACK_BISHOP = pygame.transform.smoothscale(PIECE, (SQUARE_SIZE, SQUARE_SIZE))
# S = pygame.image.load('ChessPython/images/pieces/space.png')

B_KING = svgh.load_and_scale_svg('images/pieces/black_king.svg', PIECE_SCALING)
B_QUEEN= svgh.load_and_scale_svg('images/pieces/black_queen.svg', PIECE_SCALING)
B_ROOK = svgh.load_and_scale_svg('images/pieces/black_rook.svg', PIECE_SCALING)
B_BISHOP = svgh.load_and_scale_svg('images/pieces/black_bishop.svg', PIECE_SCALING)
B_KNIGHT = svgh.load_and_scale_svg('images/pieces/black_knight.svg', PIECE_SCALING)
B_PAWN = svgh.load_and_scale_svg('images/pieces/black_pawn.svg', PIECE_SCALING)

W_KING = svgh.load_and_scale_svg('images/pieces/white_king.svg', PIECE_SCALING)
W_QUEEN = svgh.load_and_scale_svg('images/pieces/white_queen.svg', PIECE_SCALING)
W_ROOK = svgh.load_and_scale_svg('images/pieces/white_rook.svg', PIECE_SCALING)
W_BISHOP = svgh.load_and_scale_svg('images/pieces/white_bishop.svg', PIECE_SCALING)
W_KNIGHT = svgh.load_and_scale_svg('images/pieces/white_knight.svg', PIECE_SCALING)
W_PAWN = svgh.load_and_scale_svg('images/pieces/white_pawn.svg', PIECE_SCALING)


class GUI():

    def __init__(self) -> None:
        self.board = Board()
        self.move = Move()
        self.whiteToMove = True

    def draw_window(self, board):
        global SQUARE_SEL
        WIN.fill(WHITE)
        for row in range(8):
            for col in range(8):
                if SQUARE_SEL[0] == col and SQUARE_SEL[1] == row:
                    pygame.draw.rect(
                        WIN, GREEN, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        )
                elif (row % 2 == 0 and col % 2 == 1) or (row % 2 == 1 and col % 2 ==0):
                    pygame.draw.rect(
                        WIN, BROWN, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        )
                else:
                    pygame.draw.rect(
                        WIN, WHITE, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        )
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)

                if isinstance(piece, Pawn):
                    if piece.color == "black":
                        WIN.blit(B_PAWN, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                    else:
                        WIN.blit(W_PAWN, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                elif isinstance(piece, Knight):
                    if piece.color == "black":
                        WIN.blit(B_KNIGHT, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                    else:
                        WIN.blit(W_KNIGHT, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                elif isinstance(piece, Bishop):
                    if piece.color == "black":
                        WIN.blit(B_BISHOP, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                    else:
                        WIN.blit(W_BISHOP, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                elif isinstance(piece, Rook):
                    if piece.color == "black":
                        WIN.blit(B_ROOK, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                    else:
                        WIN.blit(W_ROOK, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                elif isinstance(piece, Queen):
                    if piece.color == "black":
                        WIN.blit(B_QUEEN, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                    else:
                        WIN.blit(W_QUEEN, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                elif isinstance(piece, King):
                    if piece.color == "black":
                        WIN.blit(B_KING, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                    else:
                        WIN.blit(W_KING, (col * SQUARE_SIZE, row * SQUARE_SIZE))             

        pygame.display.update()

    def reset_SEL(self) -> None:
        global SQUARE_SEL
        SQUARE_SEL[0] = -1
        SQUARE_SEL[1] = -1

    def promote_pawn(self, piece: Pawn) -> None:
        pawn_p = pp()
        choice = pawn_p.loop()

        # choice = "queen"
        match choice:
            case "queen":
                self.board.pawn_promotion(piece.color, self.board.board[piece.row][piece.col], Queen(piece.row, piece.col, piece.color))
            case "rook":
                self.board.board[piece.row][piece.col] = Rook(piece.row, piece.col, piece.color)
            case "bishop":
                self.board.board[piece.row][piece.col] = Bishop(piece.row, piece.col, piece.color)
            case "knight":
                self.board.board[piece.row][piece.col] = Knight(piece.row, piece.col, piece.color)
            case _:
                print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
                self.promote_pawn(piece)

    def gameLoop(self) -> None:
        # board = Board()
        # move = Move()
        # white_to_move = True
        global MOUSE_CLICKED

        play = True
        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False

            if event.type == pygame.MOUSEBUTTONDOWN and not MOUSE_CLICKED:
                MOUSE_CLICKED = True
                pos = pygame.mouse.get_pos()
                xpos = math.ceil(pos[0] / SQUARE_SIZE - 1)
                ypos = math.ceil(pos[1] / SQUARE_SIZE - 1)
                global SQUARE_SEL

                if SQUARE_SEL[0] == -1:
                    SQUARE_SEL[0] = xpos
                    SQUARE_SEL[1] = ypos
                else:
                    self.move.define_move(SQUARE_SEL[1], SQUARE_SEL[0], ypos, xpos)
                    if (self.whiteToMove and self.board.get_piece(self.move.start_row, self.move.start_col).color == "black") or (self.whiteToMove is False and self.board.get_piece(self.move.start_row, self.move.start_col).color == "white"):
                        print(Fore.RED + "Wrong Color!" + Style.RESET_ALL)
                        self.reset_SEL()
                        continue
                    result = self.board.move_piece(self.move, self.whiteToMove)
                    self.reset_SEL()
                
                    match result:
                        # if the move was successful
                        case Result.OK:
                            self.whiteToMove = not self.whiteToMove
                        case Result.ILLEGAL:
                            self.reset_SEL()
                            print(Fore.RED + "That was an invalid move, please make a legal move" + Style.RESET_ALL)
                        case Result.CHECK:
                            self.reset_SEL()
                            print(Fore.RED + "King is in Check!" + Style.RESET_ALL)
                        case Result.PROMOTE:
                            self.promote_pawn(self.board.get_piece(self.move.end_row, self.move.end_col))
                            self.whiteToMove = not self.whiteToMove
                            # print(self.board.__str__())
                        case Result.CHECKMATE:
                            print(Fore.RED + "Checkmate! " + "White wins!" if self.whiteToMove else "Black wins!" + Style.RESET_ALL)
                            break
                

            if event.type == pygame.MOUSEBUTTONUP and MOUSE_CLICKED:
                MOUSE_CLICKED = False

                    

            self.draw_window(self.board)

# gui = GUI()
# GUI.__main__(GUI)
        # pygame.draw.Rect()