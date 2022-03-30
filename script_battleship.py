import pygame, sys
import battleships.gen_board as battleships_gen_board
import battleships.blind_script as battleships_blind_search
import battleships.genetic_script as battleships_geneticAI_search
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
            gen_object = battleships_gen_board.gen_board(dict_level[i])
            board = gen_object.get_board()
            row_constraint = gen_object.get_row_constraint()
            col_constraint = gen_object.get_col_constraint()
            
            gen = battleships_blind_search.DFS(gen_object.get_board(), gen_object.get_ship(), gen_object.get_row_constraint(), gen_object.get_col_constraint(), len(gen_object.get_board()))
            gen.solve()
            
            end_time = process_time()
            memo_info = psutil.Process(os.getpid()).memory_info().rss/(1024*1024) - itemMemory
            df = df.append({'time' : end_time - begin_time, 'memory' : memo_info, 'game' : 'Battleship','algorithm' : 'DFS','level' : dict_level[i]},ignore_index = True)


            
    for i in range(3):
        for _ in range(num_record):     
            print("\nhehe\n")
            itemMemory = psutil.Process(os.getpid()).memory_info().rss/(1024*1024)
            begin_time = process_time()
            gen_object = battleships_gen_board.gen_board(dict_level[i])
            board = gen_object.get_board()
            row_constraint = gen_object.get_row_constraint()
            col_constraint = gen_object.get_col_constraint()
            
            gen =  battleships_geneticAI_search.Genetic(gen_object.get_board(), gen_object.get_ship(), gen_object.get_row_constraint(), gen_object.get_col_constraint(), len(gen_object.get_board()))
            flag = gen.solve()
            end_time = process_time()
            memo_info = psutil.Process(os.getpid()).memory_info().rss/(1024*1024) - itemMemory
            
            if flag == True:
                df = df.append({'time' : end_time - begin_time, 'memory' : memo_info, 'game' : 'Battleship','algorithm' : 'geneticAI','level' : dict_level[i]},ignore_index = True)
            else:
                df = df.append({'time' : 'not solve', 'memory' : memo_info, 'game' : 'Battleship','algorithm' : 'geneticAI','level' : dict_level[i]},ignore_index = True)
                
    df.to_csv("csv\\result_battleship.csv") #A_start
