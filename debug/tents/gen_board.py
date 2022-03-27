import numpy as np
import copy

#define global variables
EMPTY = 0
TREE = 1
TENT = 2

#define position
dx = [0,1,0,-1,1,1,-1,-1]
dy = [1,0,-1,0,1,-1,-1,1]

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

#map dim and object tree
dim_lst = [6,8,10,15]
object_lst = [7,12,20,45]
map_dim_object = {x : y for x,y in zip(dim_lst,object_lst)}

class Board(object):
    #=========================================================
    def __init__(self,dim):
        self.dim = dim
        
        self.num_object = map_dim_object[dim]
        
        #generate board
        generate = False
        while generate is False:
            self.board = np.zeros((dim,dim),dtype = int)
            if self.place_tents() == False:
                continue
            if self.place_trees() == False:
                continue
            self.row_constraint,self.col_constraint = self.get_constraint()
            self.sol = copy.deepcopy(self.board)
            self.remove_tents()
            generate = True
    #=========================================================
    
    #=========================================================
    def place_tents(self):
        num_try = 10 #max times random initialize one position
        for _ in range(self.num_object):
            correct = False
            place = 0
            while correct is False:
                if place > num_try:
                    return False
                x = np.random.randint(0,self.dim)
                y = np.random.randint(0,self.dim)
                neighbors = get_neighbors(self.dim,x,y,8)
                if self.board[x][y] == TENT:
                    place += 1
                    continue
                flag = True
                for position in neighbors:
                    (x0,y0) = position
                    if self.board[x0][y0] == TENT:
                        place += 1
                        flag = False
                        break
                if flag == True:
                    correct = True
                    self.board[x][y] = TENT 
        return True
    #=========================================================
    
    #=========================================================
    def place_trees(self):
        self.tree_pos = []
        for x in range(self.dim):
            for y in range(self.dim):
                if self.board[x][y] == TENT:
                    correct = False
                    neighbors = get_neighbors(self.dim,x,y)
                    while correct is False:
                        for position in neighbors:
                            (x0,y0) = position
                            if self.board[x0][y0] != TREE:
                                self.board[x0][y0] = TREE
                                self.tree_pos.append(position)
                                correct = True
                                break
                        if correct == False:
                            return False
        return True
    #=========================================================
    
    #=========================================================
    def remove_tents(self):
        for x in range(self.dim):
            for y in range(self.dim):        
                if self.board[x][y] == TENT:
                    self.board[x][y] = EMPTY
    #=========================================================
    
    #=========================================================
    def get_constraint(self):
        row_constraint = np.zeros(self.dim,dtype = int)
        col_constraint = np.zeros(self.dim,dtype = int)
        for i in range(self.dim):
            for j in range(self.dim):
                if self.board[i][j] == TENT:
                    row_constraint[i] += 1
                    col_constraint[j] += 1
        return row_constraint,col_constraint
    #=========================================================
    
    #get set method:
    def get_board(self):
        return self.board
    
    def get_row_constraint(self):
        return self.row_constraint
    
    def get_col_constraint(self):
        return self.col_constraint
    
    def get_sol(self):
        return self.sol
    
    def get_num_tree(self):
        return self.num_object
    
    def get_tree_pos(self):
        return self.tree_pos
    
# if __name__ == "__main__":
#     gen_board = Board(15)
#     board = gen_board.get_board()
#     row_constraint = gen_board.get_row_constraint()
#     col_constraint = gen_board.get_col_constraint()
#     sol = gen_board.get_sol()
    
#     print(board)
#     print("row constraint: {}".format(row_constraint))
#     print("col constraint: {}".format(col_constraint))
    
#     print(sol)