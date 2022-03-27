from GUI import *
from search import *
from gen_board import *

if __name__ == "__main__":
    gb = Board(6)
    board = gb.get_board()
    row_constraint = gb.get_row_constraint()
    col_constraint = gb.get_col_constraint()
    tree_pos = gb.get_tree_pos()
    
    agent = Search(board,row_constraint,col_constraint,tree_pos)
    agent.A_star()