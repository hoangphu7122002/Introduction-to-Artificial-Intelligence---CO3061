import os
import pygame
from pygame.transform import scale
from gen_board import *
import time

#define global variables
EMPTY = 0
BLOCK = 1

blue = (104, 149, 197)
black = (0, 0, 0)
white = (255,255,255)
red = (255,69,0)

class Gui(object):
    def __init__(self,board,dim,row_constraint,col_constraint):
        self.board = board
        self.dim = dim
        self.row_constraint = row_constraint
        self.col_constraint = col_constraint
        pygame.init()
        self.window = pygame.display.set_mode((1100,800))
        self.game_font = pygame.font.Font('FileGame\\04B_19.TTF',40)
        self.window.fill(white)
        
    def draw_board(self):
        dim = self.dim
        width = 800
        height = 800
        offset = 50
        margin = 4
        
        cell_size = int((width - 2 * offset - (dim - 1) * margin) / dim)
        step = cell_size + 5
        font = pygame.font.SysFont("ubuntumono", cell_size // 2)
        coord_x = offset
        for y in range(dim):
            coord_y = offset
            for x in range(dim):
                cell = pygame.Rect(coord_x, coord_y, cell_size, cell_size)
                if self.board[x][y] == EMPTY:
                    pygame.draw.rect(self.window, blue, cell)
                elif self.board[x][y] == BLOCK:
                   pygame.draw.rect(self.window, black, cell)
                coord_y += step
            coord_x += step
        
        # Draw cells borders
        for x in range(offset, height - offset, step):
            for y in range(offset, width - offset, step):
                cell = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(self.window, black, cell, 2)

        start = offset + (cell_size // 4)
        stop = height - cell_size

        # Display row constraints
        # print(self.row_constraint)
        for y, row_constraint in zip(range(start, stop, step), self.row_constraint):
            text = font.render(str(row_constraint), True, black)
            self.window.blit(text, [offset - 2 * text.get_width(), y])

        start = offset + (cell_size // 3)
        stop = width - cell_size
        
        # Display col constraints
        # print(self.col_constraint)
        for x, col_constraint in zip(range(start, stop, step), self.col_constraint):
            text = font.render(str(col_constraint), True, black)
            self.window.blit(text, [x, offset - text.get_height()])
        
        
    def render_font(self):
        intro_surface = self.game_font.render(f'BATTLE SHIP',True,red)
        intro_rect = intro_surface.get_rect(center = (925,300))
        self.window.blit(intro_surface,intro_rect)
        
        score_surface = self.game_font.render(f'LEVEL: {self.dim}x{self.dim}',True,black)
        score_rect = score_surface.get_rect(center = (925,450))
        self.window.blit(score_surface,score_rect)
        
        high_score_surface = self.game_font.render(f'STEP: {int(0)}',True,black)
        high_score_rect = high_score_surface.get_rect(center = (925,520))
        self.window.blit(high_score_surface,high_score_rect)
        
        time_surface = self.game_font.render(f'TIME: {int(0)}',True,black)
        time_rect = time_surface.get_rect(center = (925,590))
        self.window.blit(time_surface,time_rect)
    
    def display(self,check = 0):
        pygame.init()

        self.draw_board()
        pygame.display.flip()  # Refresh display
        # if check == 0:
        #     time.sleep(1.5)
        # else:
        #     time.sleep(0.005)
        launched = True
        while launched:
            self.draw_board()
            self.render_font()
            pygame.display.flip()  # Refresh display
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    launched = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                            launched = False

if __name__ == "__main__":
    dim = 6
    gb = gen_board(dim)
    board = gb.get_board()
    row_constraint = gb.get_row_constraint()
    col_constraint = gb.get_col_constraint()
    solution = gb.get_solution()
    print(row_constraint)
    print(col_constraint)
    
    a = Gui(solution,len(board),row_constraint,col_constraint)
    a.display()
    
    