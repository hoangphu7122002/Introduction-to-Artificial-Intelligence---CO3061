from gen_board import *
import numpy as np
import copy
import time
import random
import sys

class DFS:
    def __init__(self, board, ship, row_constraint, col_constraint, dim = 6):
        self.board = np.array(board) #numpy array
        self.dim = dim
        self.row_constraint = row_constraint
        self.col_constraint = col_constraint
        self.ship = ship
        self.total_step = 0
        self.solutions = []
    def __search__(self, id_col):
        # # debug
        #print(self.board)
        self.total_step += 1
        if (id_col == self.dim):
            #accept
            # print(self.board)
            # n = int(input())
            ok = self.check()
            if (ok):

                #TODO
                #insert solution to a SET

                #my code means insert solution but it bug duplicated
                self.solutions.append(copy.deepcopy(self.board))
                
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
                if (self.board[row][id_col] == 0 and np.count_nonzero(self.board[row,:]) < self.row_constraint[row]): # we can't' check all case (another ship is too close so, we check at the end)
                    tmp -= 1
                    keep.append([row, id_col])
                    if (tmp == 0):
                        for i in range(0, len(keep)):
                            self.board[keep[i][0]][keep[i][1]] = 1
                        self.__search__(id_col + 1)
                        # reset
                        for i in range(0, len(keep)):
                            self.board[keep[i][0]][keep[i][1]] = 0
                        tmp += 1 
                        keep.pop()

    def solve(self):
        # random according to col_constraint
        # start from id_col 0
        self.__search__(0)

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
                elif self.board[r][c] == 1 and temp[r][c] == False:
                    run = [r, c]
                    leng = 0
                    ship = []
                    #only 2 direction
                     #go right
                    while (run[1] in range(0, self.dim) and self.board[run[0]][run[1]] == 1):
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
                            if (self.board[border[i][0]][border[i][1]] == 1):
                                return False
                        type_ship.append(copy.deepcopy(leng))
                        continue
                     #go down
                    # reset
                    run = [r, c]
                    leng = 0
                    ship = []
                    while (run[0] in range(0, self.dim) and self.board[run[0]][run[1]] == 1):
                        temp[run[0]][run[1]] = True
                        ship.append(copy.deepcopy(run))
                        leng += 1
                        run[0] += 1
                    border = self.get_border(ship)
                    for i in range(len(border)):
                        if (self.board[border[i][0]][border[i][1]] == 1):
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
        print("Number of solution(s): " + str(len(self.solutions)))
        for num in range(len(self.solutions)):
            print("Solution " + str(num))
            print(self.solutions[num])
    def get_total_step_search(self):
        return self.total_step
if __name__ == '__main__':
    dim = 6
    gen_object = gen_board(dim)
    board = gen_object.get_board()
    row_constraint = gen_object.get_row_constraint()
    col_constraint = gen_object.get_col_constraint()
    solutionBoard = gen_object.get_solution()
    
    print("\n==============GENERATE================\n")
    print_board(board,dim,col_constraint,row_constraint)
    print("\n======================================\n")

    print("\n==============SOLUTION================\n")
    print_board(solutionBoard,dim,col_constraint,row_constraint)
    print("\n======================================\n")

    dfs = DFS(gen_object.get_board(), gen_object.get_ship(), gen_object.get_row_constraint(), gen_object.get_col_constraint())
    dfs.solve()
    dfs.show()
    print("Total step search " +str(dfs.get_total_step_search()))