import os
import pygame
from pygame.transform import scale
from gen_board import *
import time

#define global variables
EMPTY = 0
TREE = 1
TENT = 2

red = (255,69,0)
green = (0, 255, 130)
black = (0, 0, 0)
white = (255,255,255)

class Gui(object):
    def __init__(self,board,dim,row_constraint,col_constraint):
        self.board = board
        self.dim = dim
        self.row_constraint = row_constraint
        self.col_constraint = col_constraint
        pygame.init()
        self.window = pygame.display.set_mode((1100,800))
        self.window.fill(white)
        self.game_font = pygame.font.Font('FileGame\\04B_19.TTF',40)
        self.tent_image = pygame.image.load(os.path.join('images','tent-icon.jpg')).convert()
        self.tree_image = pygame.image.load(os.path.join('images','tree-icon.png')).convert()
        
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
                    pygame.draw.rect(self.window, green, cell)
                if self.board[x][y] == TENT:
                   self.window.blit(scale(self.tent_image, (cell_size, cell_size)), cell) 
                elif self.board[x][y] == TREE:
                    self.window.blit(scale(self.tree_image, (cell_size, cell_size)), cell)
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
        for y, row_constraint in zip(range(start, stop, step), self.row_constraint):
            text = font.render(str(row_constraint), True, black)
            self.window.blit(text, [offset - 2 * text.get_width(), y])

        start = offset + (cell_size // 3)
        stop = width - cell_size
        # Display col constraints
        for x, col_constraint in zip(range(start, stop, step), self.col_constraint):
            text = font.render(str(col_constraint), True, black)
            self.window.blit(text, [x, offset - text.get_height()])
        
    def render_font(self,step = 0,time = 0,score = -1):
        intro_surface = self.game_font.render(f'TENTS PUZZLE',True,red)
        intro_rect = intro_surface.get_rect(center = (925,300))
        self.window.blit(intro_surface,intro_rect)
        
        score_surface = self.game_font.render(f'LEVEL: {self.dim}x{self.dim}',True,black)
        score_rect = score_surface.get_rect(center = (925,450))
        self.window.blit(score_surface,score_rect)
        
        high_score_surface = self.game_font.render(f'STEP: {step}',True,black)
        high_score_rect = high_score_surface.get_rect(center = (925,520))
        self.window.blit(high_score_surface,high_score_rect)
        
        time_surface = self.game_font.render(f'TIME: {time}',True,black)
        time_rect = time_surface.get_rect(center = (925,590))
        self.window.blit(time_surface,time_rect)
        
        if score != -1:
            score_depth_surface = self.game_font.render(f'SCORE: {score}',True,black)
            score_depth_rect = score_depth_surface.get_rect(center = (925,660))
            self.window.blit(score_depth_surface,score_depth_rect)
    
    def display(self,step = 0,time_ = 0,score = -1,check = 0):
        pygame.init()
        self.render_font(step,time_,score)
        self.draw_board()
        pygame.display.flip()  # Refresh display
        if check == 0:
            time.sleep(1.5)
        else:
            time.sleep(0.005)
        # launched = True
        # while launched:
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         launched = False
        #     if event.type == pygame.KEYUP:
        #         if event.key == pygame.K_ESCAPE:
        #                 launched = False

# if __name__ == "__main__":
#     gb = Board(8)
#     board = gb.get_board()
#     row_constraint = gb.get_row_constraint()
#     col_constraint = gb.get_col_constraint()
#     sol = gb.get_sol()
    
#     a = Gui(sol,len(board),row_constraint,col_constraint)
#     a.display()
    
    