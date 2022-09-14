import pygame as pg
import math

pg.init()


WIN_WIDTH, WIN_HEIGHT = 600, 600
WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Pawn Promotion")

WHITE = (255,255,255)
BLACK = (0,0,0)
BOX_WIDTH, BOX_HEIGHT = 400, 60 #100, 30
BOX_H_SPACER = 100 #50
BOX_V_SPACER = 40 #20

# MOUSE_CLICKED = False
 
font = pg.font.SysFont('timesnewroman',  30)
queen = font.render("Queen", False, WHITE, None)
rook = font.render("Rook", False, WHITE, None)
bishop = font.render("Bishop", False, WHITE, None)
knight = font.render("Knight", False, WHITE, None)

class pawn_promotion:
    # def __init__(self):
    #     return self.loop()

    def draw_window(self):
        WIN.fill(WHITE)
        pg.draw.rect(
                WIN, BLACK, pg.Rect(BOX_H_SPACER, BOX_V_SPACER * 4, BOX_WIDTH, BOX_HEIGHT))
        pg.draw.rect(
                WIN, BLACK, pg.Rect(BOX_H_SPACER, BOX_V_SPACER * 5 + BOX_HEIGHT, BOX_WIDTH, BOX_HEIGHT))
        pg.draw.rect(
                WIN, BLACK, pg.Rect(BOX_H_SPACER, BOX_V_SPACER * 6 + BOX_HEIGHT * 2, BOX_WIDTH, BOX_HEIGHT))
        pg.draw.rect(
                WIN, BLACK, pg.Rect(BOX_H_SPACER, BOX_V_SPACER * 7 + BOX_HEIGHT * 3, BOX_WIDTH, BOX_HEIGHT))
        WIN.blit(queen, (BOX_H_SPACER + BOX_WIDTH / 2, BOX_V_SPACER * 4)) 
        WIN.blit(rook, (BOX_H_SPACER + BOX_WIDTH / 2, BOX_V_SPACER * 5 + BOX_HEIGHT))      
        WIN.blit(bishop, (BOX_H_SPACER + BOX_WIDTH / 2, BOX_V_SPACER * 6 + BOX_HEIGHT * 2))      
        WIN.blit(knight, (BOX_H_SPACER + BOX_WIDTH / 2, BOX_V_SPACER * 7 + BOX_HEIGHT * 3))            
        pg.display.update()

    def loop(self):
        # play = True
        # pieceChosen = ""
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    play = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    xpos = pos[0]
                    ypos = pos[1]
                    if (xpos > BOX_H_SPACER and xpos < BOX_H_SPACER + BOX_WIDTH 
                        and ypos > BOX_V_SPACER * 4 and ypos < BOX_V_SPACER * 4 + BOX_HEIGHT):
                        return "queen"
                    elif (xpos > BOX_H_SPACER and xpos < BOX_H_SPACER + BOX_WIDTH 
                        and ypos > BOX_V_SPACER * 5 + BOX_HEIGHT and ypos < BOX_V_SPACER * 5 + BOX_HEIGHT * 2):
                        return "rook"
                    elif (xpos > BOX_H_SPACER and xpos < BOX_H_SPACER + BOX_WIDTH 
                        and ypos > BOX_V_SPACER * 6 + BOX_HEIGHT * 2 and ypos < BOX_V_SPACER * 6 + BOX_HEIGHT * 3):
                        return "bishop"
                    elif (xpos > BOX_H_SPACER and xpos < BOX_H_SPACER + BOX_WIDTH 
                        and ypos > BOX_V_SPACER * 7 + BOX_HEIGHT * 3 and ypos < BOX_V_SPACER * 7 + BOX_HEIGHT * 4):
                        return "knight"

            self.draw_window()
