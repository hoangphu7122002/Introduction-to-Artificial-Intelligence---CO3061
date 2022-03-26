from gen_board import *

def check(board, row_constraint, col_constraint, ships):
    dim = len(board)
    ships_board = []
    row_board = np.zeros(dim, dtype=int)
    col_board = np.zeros(dim, dtype=int)
    
    for x in range(dim):
        for y in range(dim):
            pass
        
