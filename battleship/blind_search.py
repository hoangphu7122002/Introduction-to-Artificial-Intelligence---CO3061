import numpy as np
import copy
import time
import random

dx = [0,1,0,-1,1,1,-1,-1]
dy = [1,0,-1,0,1,-1,-1,1]

#define global variable
EMPTY = 0
BLOCK = 1
MAX_TRIES = 10 #for gen ele

#helperFunction
#=========================================================
def check_in_board(x,y,dim):
    if x < 0 or x >= dim:
        return False
    if y < 0 or y >= dim:
        return False
    return True
#=========================================================    

#=========================================================
def get_neighbors(dim,x,y,ele = 4):
    neighbors = []
    for k in range(ele):
        new_x = x + dx[k]
        new_y = y + dy[k]
        if check_in_board(new_x,new_y,dim) is True:
            neighbors.append((new_x,new_y))
    return neighbors
#=========================================================

#=========================================================
def print_board(board,dim,col_constraint,row_constraint):
        head_col = "     "
        for ele in col_constraint:
            head_col += str(ele)
            head_col += ' '
        line = "    "
        line += "-" * 13
        line += '\n'
        head_col += '\n'
        head_col += line
        row = [""] * dim
        index = 0
        for i in range(dim):
            row[i] += str(row_constraint[i])
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
#=========================================================

#=========================================================
def gen_tail(head,ship_len):
    #gen direction of board
    #left - L: 0
    #right - R: 1
    #down: - D: 2
    #up: - U: 3
    direction = np.random.randint(0,4)
    if direction == 0:
        tail = (head[0] - ship_len + 1, head[1])
    elif direction == 1:
        tail = (head[0] + ship_len - 1, head[1])
    elif direction == 2:
        tail = (head[0], head[1] - ship_len + 1)
    elif direction == 3:
        tail = (head[0], head[1] + ship_len - 1)
    return tail
#=========================================================

class gen_board(object):
    #=========================================================
    def __init__(self,dim = 6):
        self.ship = None
        if dim == 6:
            self.ship = [3,2,2,1,1,1]
        elif dim == 8: 
            self.ship = [4,3,3,2,2,2,1,1,1]
        else: 
            self.ship = [4,3,3,2,2,2,1,1,1,1]
        self.dim = dim
        generate = False
        while not generate:
            self.board = np.zeros((dim,dim))
            if self.placed_block() == False:
                continue
            self.row_constraint,self.col_constraint = self.gen_constraint()
            self.remove_block()
            generate = True
    #=========================================================
    
    #=========================================================
    def placed_block(self):
        self.pos_block = []
        for ship_len in self.ship:
            #generate head of the ship
            correct = False
            num_try = 0
            while not correct:
                if num_try >= MAX_TRIES:
                    return False
                head_x = np.random.randint(0,self.dim)
                head_y = np.random.randint(0,self.dim)
                
                head = (head_x,head_y)
                
                if self.board[head_x][head_y] == BLOCK:
                    num_try += 1
                    continue 
                    
                tail = gen_tail(head,ship_len)
                if check_in_board(tail[0],tail[1],self.dim) == False:
                    num_try += 1
                    continue
                if self.board[tail[0]][tail[1]] == BLOCK:
                    num_try += 1
                    continue
                #identify block
                x_min_block = min(head[0],tail[0])
                x_max_block = max(head[0],tail[0])
                y_min_block = min(head[1],tail[1])
                y_max_block = max(head[1],tail[1])
                
                #check neighbor have no block
                flag = True
                for x in range(x_min_block,x_max_block + 1):
                    for y in range(y_min_block,y_max_block + 1):
                        if self.board[x][y] == BLOCK:  
                            num_try += 1
                            flag = False
                            break
                        neighbors = get_neighbors(self.dim,x,y,8)
                        for postion in neighbors:
                            if self.board[postion[0]][postion[1]] == BLOCK: 
                                num_try += 1
                                flag = False
                                break
                    if flag == False:
                        break
                if flag == True:
                    self.board[x_min_block : (x_max_block + 1),y_min_block : (y_max_block + 1)] = BLOCK
                    correct = True    
                    self.pos_block.append((x_min_block,y_min_block,x_max_block,y_max_block))
        self.solution = copy.deepcopy(self.board)
        return True
    #========================================================
                    
    #========================================================
    def gen_constraint(self):
        row_constraint = np.zeros(self.dim,dtype = int)
        col_constraint = np.zeros(self.dim,dtype = int)
        for x in range(self.dim):
            for y in range(self.dim):
                if self.board[x][y] == BLOCK:   
                    row_constraint[x] += 1
                    col_constraint[y] += 1
        return row_constraint,col_constraint
   #========================================================
    
    #========================================================
    def remove_block(self):
        num_hint_block = None
        if self.dim == 6:
            num_hint_block = np.random.randint(1,4)
        elif self.dim == 8:
            num_hint_block = np.random.randint(2,5)
        else:
            num_hint_block = np.random.random(3,6)
        print(self.pos_block)
        random.shuffle(self.pos_block)
        for i in range(len(self.pos_block)):
            x_min,y_min,x_max,y_max = self.pos_block[i]
            if i < num_hint_block:
                hint_block_x = np.random.randint(x_min,x_max + 1)
                hint_block_y = np.random.randint(y_min,y_max + 1)
                self.board[x_min : x_max + 1,y_min : y_max + 1] = EMPTY
                self.board[hint_block_x][hint_block_y] = BLOCK
            else:
                self.board[x_min : x_max + 1,y_min : y_max + 1] = EMPTY
    #========================================================
    
    #========================================================
    #get method
    def get_board(self):
        return self.board
    
    def get_solution(self):
        return self.solution
    
    def get_row_constraint(self):
        return self.row_constraint
    
    def get_col_constraint(self):
        return self.col_constraint
    
    def get_pos_block(self):
        return self.pos_block
    
    def get_ship(self):
        return self.ship
    #========================================================
    
solutionBoard = None

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
    
