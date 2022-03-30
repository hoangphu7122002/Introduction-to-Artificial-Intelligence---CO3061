import pygame, sys
import tents.gen_board as tents_gen_board
import tents.search_script as tents_search
from time import process_time
import pandas as pd
import numpy as np
import os
import psutil
dict_level = {0 : 6,
              1 : 8,
              2 : 10}
num_record = 5

if __name__ == "__main__":
    #DFS
    
    df = pd.DataFrame(columns = ['time','memory','game','algorithm','level'])
    
    for i in range(3):
        for _ in range(num_record):        
            print("\nhehe\n")
            itemMemory = psutil.Process(os.getpid()).memory_info().rss/(1024*1024)
            begin_time = process_time()
            gb = tents_gen_board.Board(dict_level[i])
            board = gb.get_board()
            row_constraint = gb.get_row_constraint()
            col_constraint = gb.get_col_constraint()
            tree_pos = gb.get_tree_pos()
            
            agent = tents_search.Search(board,row_constraint,col_constraint,tree_pos)
            agent.DFS()
            end_time = process_time()
            memo_info = psutil.Process(os.getpid()).memory_info().rss/(1024*1024) - itemMemory
            df = df.append({'time' : end_time - begin_time, 'memory' : memo_info, 'game' : 'Tents','algorithm' : 'DFS','level' : dict_level[i]},ignore_index = True)


            
    for i in range(3):
        for _ in range(num_record):     
            print("\nhehe\n")
            itemMemory = psutil.Process(os.getpid()).memory_info().rss/(1024*1024)
            begin_time = process_time()
            gb = tents_gen_board.Board(dict_level[i])
            board = gb.get_board()
            row_constraint = gb.get_row_constraint()
            col_constraint = gb.get_col_constraint()
            tree_pos = gb.get_tree_pos()
            
            agent = tents_search.Search(board,row_constraint,col_constraint,tree_pos)
            agent.A_star()
            end_time = process_time()
            memo_info = psutil.Process(os.getpid()).memory_info().rss/(1024*1024) - itemMemory
            
            df = df.append({'time' : end_time - begin_time, 'memory' : memo_info, 'game' : 'Tents','algorithm' : 'A_star','level' : dict_level[i]},ignore_index = True)

    df.to_csv("csv\\result_tent.csv")
    #A_start