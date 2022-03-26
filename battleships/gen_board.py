import numpy as np
import copy
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
        line += "-" * map_line_dim[dim]
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
        line += "-" * map_line_dim[dim]
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

#============================================================
dim_lst = [6,8,10,15]
ship_lst = [[3,2,2,1,1,1],[4,3,3,2,2,2,1,1,1],[4,3,3,2,2,2,1,1,1,1],[5,4,4,3,3,3,2,2,2,2,1,1,1,1,1]]
map_dim_ship = {x : y for x,y in zip(dim_lst,ship_lst)}

random_hint = [(1,4),(2,5),(3,6),(8,11)]
map_hint_dim = {x : y for x,y in zip(dim_lst,random_hint)}

line_lst = [13,17,21,31]
map_line_dim = {x : y for x,y in zip(dim_lst,line_lst)}
#============================================================

class gen_board(object):
    #=========================================================
    def __init__(self,dim = 6):
        self.dim = dim
        self.ship = map_dim_ship[self.dim]
        
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
        begin,end = map_hint_dim[self.dim]
        num_hint_block = np.random.randint(begin,end)
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

if __name__ == '__main__':
    dim = 6
    gen_object = gen_board(dim)
    board = gen_object.get_board()
    row_constraint = gen_object.get_row_constraint()
    col_constraint = gen_object.get_col_constraint()
    solution = gen_object.get_solution()
    
    print(gen_object.get_ship())
    
    print("\n==============GENERATE================\n")
    print_board(board,dim,col_constraint,row_constraint)
    print("\n======================================\n")
    
    print("\n==============SOLUTION================\n")
    print_board(solution,dim,col_constraint,row_constraint)
    print("\n======================================\n")
            
                                
                
                
                
                
            