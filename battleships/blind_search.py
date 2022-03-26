from gen_board import *
from GUI import *
import numpy as np
import copy
from time import process_time
import random

solutionBoard = None
EMPTY = 0
BLOCK = 1

class DFS:
    def __init__(self, board, ship, row_constraint, col_constraint, dim = 6):
        self.board = np.array(board) #numpy array
        self.initboard = copy.deepcopy(self.board)
        self.prtSolutionBoard = np.array(board)
        self.dim = dim
        self.row_constraint = row_constraint
        self.col_constraint = col_constraint
        self.ship = ship
        self.total_step = 0
        self.solution = []
        self.interupt = None
        self.begin_time = process_time()
        self.stop_time = 0
    def __search__(self, id_col):
        # # debug
        #print(self.board)
        if (self.solution != []):# or self.interupt != None
            return
        prt = Gui(self.board,self.dim,self.row_constraint,self.col_constraint)
        self.stop_time = process_time()
        prt.display(self.total_step, self.stop_time - self.begin_time, 0.005)
        if (prt.interupt()):
            self.interupt = True
        self.total_step += 1
        if (id_col == self.dim):
            #accept
            # print(self.board)
            # n = int(input())
            ok = self.check()
            if (ok):
                self.solution.append(copy.deepcopy(self.board))
                self.stop_time = process_time() - self.begin_time
            return
        remain = self.col_constraint[id_col] - np.count_nonzero(self.board[:,id_col])
        # # debug
        # print(self.board[:,id_col])
        # print("column " + str(id_col) +" remain = " + str(remain))
        keep = []
        if (remain <= 0):
            self.__search__(id_col + 1)
            return

        for t in range(0, self.dim):
            keep = []
            tmp = copy.deepcopy(remain)
            for row in range(t, self.dim):
                if (self.board[row][id_col] == EMPTY and np.count_nonzero(self.board[row,:]) < self.row_constraint[row]): # we can't' check all case (another ship is too close so, we check at the end)
                    tmp -= 1
                    keep.append([row, id_col])
                    if (tmp == 0):
                        for i in range(0, len(keep)):
                            self.board[keep[i][0]][keep[i][1]] = BLOCK
                        self.__search__(id_col + 1)
                        # reset
                        for i in range(0, len(keep)):
                            self.board[keep[i][0]][keep[i][1]] = EMPTY
                        tmp += 1 
                        keep.pop()
    def solve(self):
        # random according to col_constraint
        # start from id_col 0
        self.__search__(0)
        # display solution
        if (self.solution != []):           
            print("===== SOLUTION =====")
            init = Gui(self.prtSolutionBoard,self.dim,self.row_constraint,self.col_constraint)
            init.display(self.total_step, self.stop_time)
            vis = np.zeros((self.dim, self.dim))
            for i in range(0, self.dim):
                for j in range(0, self.dim):
                    if (self.solution[0][i][j] == BLOCK and vis[i][j] == 0):
                        ii = copy.deepcopy(i)
                        jj = copy.deepcopy(j)
                        while (ii in range(0, self.dim) and self.solution[0][ii][jj] == BLOCK):
                            self.prtSolutionBoard[ii][jj] = BLOCK
                            vis[ii][jj] = 1
                            ii += 1
                        ii = copy.deepcopy(i)
                        jj = copy.deepcopy(j)
                        while (jj in range(0, self.dim) and self.solution[0][ii][jj] == BLOCK):
                            self.prtSolutionBoard[ii][jj] = BLOCK
                            vis[ii][jj] = 1
                            jj += 1
                        gui_board = Gui(self.prtSolutionBoard,self.dim,self.row_constraint,self.col_constraint)
                        gui_board.display(self.total_step, self.stop_time)
            gui_board = Gui(self.prtSolutionBoard,self.dim,self.row_constraint,self.col_constraint)
            gui_board.display(self.total_step, self.stop_time, 0)
    def get_border(self, ship):
        border = []
        for sh in range(0, len(ship)):
            neigh = get_neighbors(self.dim, ship[sh][0], ship[sh][1], 8)
            for ne in range(0, len(neigh)):
                if (not list(neigh[ne]) in ship and not neigh[ne] in border):
                    border.append(neigh[ne])
        return border
    def check(self):
        # not over constraint
        for i in range(self.dim):
            if (np.count_nonzero(self.board[:,i]) != self.col_constraint[i]):
                return False
            if (np.count_nonzero(self.board[i,:]) != self.row_constraint[i]):
                return False
        
        # not appear too close
        temp = np.zeros((self.dim, self.dim))
        type_ship = []
        for r in range(self.dim):
            for c in range(self.dim):
                if (self.board[r][c] == 0):
                    temp[r][c] = True
                elif self.board[r][c] == BLOCK and temp[r][c] == False:
                    run = [r, c]
                    leng = 0
                    ship = []
                    #only 2 direction
                     #go right
                    while (run[1] in range(0, self.dim) and self.board[run[0]][run[1]] == BLOCK):
                        temp[run[0]][run[1]] = True
                        ship.append(copy.deepcopy(run))
                        leng += 1
                        run[1] += 1
                    if leng > 1: # clearly known direction is go right
                        border = self.get_border(ship)
                        # print("ship") 
                        # print(ship)
                        # print("border")
                        # print(border)
                        for i in range(len(border)):
                            if (self.board[border[i][0]][border[i][1]] == BLOCK):
                                return False
                        type_ship.append(copy.deepcopy(leng))
                        continue
                     #go down
                    # reset
                    run = [r, c]
                    leng = 0
                    ship = []
                    while (run[0] in range(0, self.dim) and self.board[run[0]][run[1]] ==BLOCK):
                        temp[run[0]][run[1]] = True
                        ship.append(copy.deepcopy(run))
                        leng += 1
                        run[0] += 1
                    border = self.get_border(ship)
                    for i in range(len(border)):
                        if (self.board[border[i][0]][border[i][1]] == BLOCK):
                            return False
                    type_ship.append(copy.deepcopy(leng))

        # enough type of ship
        type_ship.sort()
        type_ship.reverse()
        # print("type ship")
        # print(type_ship)
        for i in range(len(type_ship)):
            if (type_ship[i] != self.ship[i]):
                return False
        return True
    def show(self):
        if (self.solution != []):
            print_board(self.solution[0], self.dim, self.col_constraint, self.row_constraint)
        else:
            print("No solution found!")
    def get_total_step_search(self):
        return self.total_step

######## debug ##########

# if __name__ == '__main__':
#     dim = 6
#     gen_object = gen_board(dim)
#     board = gen_object.get_board()
#     row_constraint = gen_object.get_row_constraint()
#     col_constraint = gen_object.get_col_constraint()
#     solutionBoard = gen_object.get_solution()
    
#     print("\n==============GENERATE================\n")
#     print_board(board,dim,col_constraint,row_constraint)
#     print("\n==============SOLUTION================\n")
#     print_board(solutionBoard,dim,col_constraint,row_constraint)
#     print("\n======================================\n")

#     dfs = DFS(gen_object.get_board(), gen_object.get_ship(), gen_object.get_row_constraint(), gen_object.get_col_constraint(), dim)
#     dfs.solve()
#     dfs.show()
#     print("Total step search " +str(dfs.get_total_step_search()))
    
