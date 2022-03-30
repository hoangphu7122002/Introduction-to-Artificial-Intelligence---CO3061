from re import L
import numpy as np
from tents.gen_board import *
from queue import PriorityQueue
import copy
from tents.GUI import *
from time import process_time

# np.random.seed(0)

#define global variables
EMPTY = 0
TREE = 1
TENT = 2

class Search(object):
    def __init__(self,board,row_constraint,col_constraint,tree_pos):
        self.dim = len(board)
        self.board = board
        self.row_constraint = row_constraint
        self.col_constraint = col_constraint
        self.tree_pos = tree_pos
        self.num_tree = len(tree_pos)
        self.step = 0 #count step to converge optimal solution
        self.begin_time = process_time()
        
    #HELPER FUNCTION
    #=============================================================
    def zip_board(self,board):
        string_ele = ""
        for i in range(len(board)):
            for j in range(len(board)):
                string_ele += str(board[i][j])
                string_ele += ' '
        return string_ele
    
    def unzip_board(self,str):
        board = np.zeros((self.dim,self.dim))
        ele = str.strip().split()
        for i in range(len(board)):
            for j in range(len(board)):
                board[i][j] = int(float(ele[i * self.dim + j]))
        return board
    #=============================================================
    
    #A_STAR ALGORITHM
    #================================================================
    def A_star(self):
        self.open_list = PriorityQueue() #has tuple (score, depth, board_compress)
        score = self.score(self.board)
        self.open_list.put((score + 0,0,self.zip_board(self.board)))
        while not self.open_list.empty():
            score,depth,board = self.open_list.get()
            board = self.unzip_board(board)
            if depth == self.num_tree:
                if score == depth:
                    #backtrack to sol
                    self.back_track_solution(board)
                    return
            #fill
            gui_board = Gui(board,self.dim,self.row_constraint,self.col_constraint)
            if self.interupt() is None:
                return None
            self.stop_time = process_time()
            gui_board.display(self.step,(self.stop_time - self.begin_time),score + depth,1)
            if depth < self.num_tree:
                (x,y) = self.tree_pos[depth]
                neighbors = get_neighbors(self.dim,x,y,4)
                for position in neighbors:
                    (x_nei,y_nei) = position
                    if board[x_nei][y_nei] == EMPTY:
                        board[x_nei][y_nei] = TENT 
                        score_tent = self.score(board) + depth + 1
                        self.open_list.put((score_tent,depth + 1,self.zip_board(board)))
                        board[x_nei][y_nei] = EMPTY
                        self.step += 1
        print("\n============NO SOLUTION============\n")
        return False
    #================================================================
    
    #SCORE FOR CHECK SOLUTION OR HEURISTIC FOR A_STAR
    #====================================================
    def score(self,board):
        row_count = np.zeros(self.dim,dtype=int)
        col_count = np.zeros(self.dim,dtype=int)
        
        tent_violate = 0    
        check_pair = set()
        
        for x in range(self.dim):
            for y in range(self.dim):
            
                if board[x][y] == TENT:
                    row_count[x] += 1
                    col_count[y] += 1
                    neighbors = get_neighbors(self.dim,x,y,8)
                    for position in neighbors:
                        x0,y0 = position
                        if board[x0][y0] == TENT:
                            tent_violate += 1
                            
                if board[x][y] == TREE:
    
                    neighbors = get_neighbors(self.dim,x,y,4)
                    for position in neighbors:
                        x0,y0 = position
                        if board[x0][y0] == TENT:
                            check_pair.add(position)
            
        pair_violate = self.num_tree - len(check_pair)
        constraint_violate = 0
        for i in range(len(row_count)):
            score = abs(row_count[i] - self.row_constraint[i])
            constraint_violate += score
        
        for j in range(len(col_count)):
            score = abs(col_count[j] - self.col_constraint[j])
            constraint_violate += score
        tent_violate = tent_violate // 2
        return pair_violate + constraint_violate + tent_violate
    #====================================================
    
    #INFORMED SEARCH
    #===================================================
    def DFS(self):
        board = copy.deepcopy(self.board)
        return self.DFS_recursion(board,0)
        
    def interupt(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # throw: Exception("interupt program")
                return None
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    # throw: Exception("interupt program")
                    return None
        return True
    
    def DFS_recursion(self,board,depth):
        gui_board = Gui(board,self.dim,self.row_constraint,self.col_constraint)
        if self.interupt() is None:
            return None
        self.stop_time = process_time()
        gui_board.display(self.step,(self.stop_time - self.begin_time) ,depth,1)
        # print(depth)
        if depth == self.num_tree:
            score = self.score(board)
            if score == 0:
                #backtrack to sol
                self.back_track_solution(board)
                return
        if depth < self.num_tree:
            (x,y) = self.tree_pos[depth]
            neighbors = get_neighbors(self.dim,x,y,4)
            for position in neighbors:
                (x_nei,y_nei) = position
                if board[x_nei][y_nei] == EMPTY and np.count_nonzero(board[:,y_nei] == TENT) < self.col_constraint[y_nei] and np.count_nonzero(board[x_nei, :]  == TENT) < self.row_constraint[x_nei]:
                    board[x_nei][y_nei] = TENT 
                    self.DFS_recursion(board,depth + 1)
                    board[x_nei][y_nei] = EMPTY
                    self.step += 1
    #===================================================
    
    #PRINT SOLUTION
    #==================================================
    def back_track_solution(self,solution):
        tent_pos = []
        for x in range(self.dim):
            for y in range(self.dim):
                if solution[x][y] == TENT:
                    tent_pos.append((x,y))
        print("\n===========SOLUTION==========\n")
        # self.print_board(self.board)
        gui_board = Gui(self.board,self.dim,self.row_constraint,self.col_constraint)
        if self.interupt() is None:
            return None
        self.stop_time = process_time()
        gui_board.display(self.step,(self.stop_time - self.begin_time),-1 ,0)
        total_time = (self.stop_time - self.begin_time)
        for i in range(len(tent_pos)):
            print("\n=========STEP{}========\n".format(i + 1))
            x,y = tent_pos[i]
            self.board[x][y] = TENT
            # self.print_board(self.board)
            gui_board = Gui(self.board,self.dim,self.row_constraint,self.col_constraint)
            if self.interupt() is None:
                return None
            self.stop_time = process_time()
            gui_board.display(self.step,total_time,-1,0)
            
        
        launch = True
        while launch :
            gui_board = Gui(self.board,self.dim,self.row_constraint,self.col_constraint)
            gui_board.display(self.step,total_time,-1,0)
            if self.interupt() == None:
                launch = False
        print("\nnum_step: {}\n".format(self.step))
        print("\n==========END===========\n")
    
    def print_board(self,board):
        head_col = "     "
        for ele in self.col_constraint:
            head_col += str(ele)
            head_col += ' '
        line = "    "
        line += "-" * 13
        line += '\n'
        head_col += '\n'
        head_col += line
        row = [""] * self.dim
        index = 0
        for i in range(self.dim):
            row[i] += str(self.row_constraint[i])
            row[i] += '  | '
            for ele in board[index]:
                row[i] += str(int(ele))
                row[i] += ' '
            row[i] += '|\n'
            index += 1
        for ele in row:
            head_col += ele
        line = "    "
        line += "-" * 13
        line += '\n'
        head_col += line
        print(head_col)
    #==================================================


    
    
    
    
