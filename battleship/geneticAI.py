from gen_board import *
import time
import numpy as np

class Genetic:
    def __init__(self, board, ship, row_constraint, col_constraint, dim = 6):
        self.board = np.array(board) #numpy array
        self.dim = dim
        self.row_constraint = row_constraint
        self.col_constraint = col_constraint
        self.ship = ship
        self.total_step = 0
        self.solutions = []
        self.gen = []     
        
    def __search__(self, board):
        cur_diff = 0
        for row in range(self.dim):
            if (np.count_nonzero(self.board[row, :]) == self.row_constraint[row]):
                cur_diff += 1
    def get_border(self, ship):
        border = []
        for sh in range(0, len(ship)):
            neigh = get_neighbors(self.dim, ship[sh][0], ship[sh][1], 8)
            for ne in range(0, len(neigh)):
                if (not list(neigh[ne]) in ship and not neigh[ne] in border):
                    border.append(neigh[ne])
        return border   
        
    def get_ship_present(self,board):
        temp = np.zeros((self.dim, self.dim))
        type_ship = []
        for r in range(self.dim):
            for c in range(self.dim):
                if (board[r][c] == 0):
                    temp[r][c] = True
                elif board[r][c] == 1 and temp[r][c] == False:
                    run = [r, c]
                    leng = 0
                    ship = []
                    #only 2 direction
                     #go right
                    while (run[1] in range(0, self.dim) and board[run[0]][run[1]] == 1):
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
                            if (board[border[i][0]][border[i][1]] == 1):
                                return False
                        type_ship.append(copy.deepcopy(leng))
                        continue
                     #go down
                    # reset
                    run = [r, c]
                    leng = 0
                    ship = []
                    while (run[0] in range(0, self.dim) and board[run[0]][run[1]] == 1):
                        temp[run[0]][run[1]] = True
                        ship.append(copy.deepcopy(run))
                        leng += 1
                        run[0] += 1
                    border = self.get_border(ship)
                    for i in range(len(border)):
                        if (board[border[i][0]][border[i][1]] == 1):
                            return False
                    type_ship.append(copy.deepcopy(leng))

        # enough type of ship
        type_ship.sort()
        type_ship.reverse()
        # print("type ship")
        # print(type_ship)
        point = 0
        
        for i in range(min(len(type_ship),len(self.ship))):
            if (type_ship[i] != self.ship[i]):
                point += abs(type_ship[i] - self.ship[i])
        
        if len(type_ship) > len(self.ship):
            max_t = type_ship
            min_t = self.ship
        else:
            min_t = type_ship
            max_t = self.ship
        
        for i in range(len(min_t),len(max_t)):
            point += max_t[i]
        
        return point

    def check(self, state):
        # not over constraint
        for i in range(self.dim):
            if (np.count_nonzero(state[:,i]) != self.col_constraint[i]):
                return False
            if (np.count_nonzero(state[i,:]) != self.row_constraint[i]):
                return False
        # not appear too close
        # not appear too close
        temp = np.zeros((self.dim, self.dim))
        type_ship = []
        for r in range(self.dim):
            for c in range(self.dim):
                if (state[r][c] == 0):
                    temp[r][c] = True
                elif state[r][c] == 1 and temp[r][c] == False:
                    run = [r, c]
                    leng = 0
                    ship = []
                    #only 2 direction
                     #go right
                    while (run[1] in range(0, self.dim) and state[run[0]][run[1]] == 1):
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
                            if (state[border[i][0]][border[i][1]] == 1):
                                return False
                        type_ship.append(copy.deepcopy(leng))
                        continue
                     #go down
                    # reset
                    run = [r, c]
                    leng = 0
                    ship = []
                    while (run[0] in range(0, self.dim) and state[run[0]][run[1]] == 1):
                        temp[run[0]][run[1]] = True
                        ship.append(copy.deepcopy(run))
                        leng += 1
                        run[0] += 1
                    border = self.get_border(ship)
                    for i in range(len(border)):
                        if (state[border[i][0]][border[i][1]] == 1):
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
        
        
    def generate_board(self):
        # generate random board enough part of ship in all of rows
        # loop through rows
        board2 = copy.deepcopy(self.board)
        for row in range(self.dim):
            # calculate remain part of ships need
            remain = self.row_constraint[row] - np.count_nonzero(board2[row, :])
            # put each of them to random index
            for put in range(remain):
                col = np.random.randint(0, self.dim)
                while (board2[row][col] == 1):
                    col = np.random.randint(0, self.dim)
                board2[row][col] = 1
        return board2
        
    def fitness(self, state):
        cnt = 0
        for c in range(self.dim):
            cnt += np.count_nonzero(state[:, c]) == self.col_constraint[c] 
        cnt += self.get_ship_present(state)
        return cnt
        
    def fitness_comp(self, state):
        return self.fitness(state)
        
    def solve(self):
        num_of_populations = 50
        done = False
        for i in range(num_of_populations):
            self.gen.append(self.generate_board())
        self.gen.sort(key = self.fitness_comp, reverse = True)
        ans = None
        generation = 0
        # getting started generation
        while not done:
            print("Generation " + str(generation))
            generation += 1
            # selections, random 2 index, choice better
            # for i in range(0, num_of_populations):
            #     inx1 = np.random.randint(0, num_of_populations)
            #     inx2 = np.random.randint(0, num_of_populations)
            #     while inx2 == inx1:
            #         inx2 = np.random.randint(0, num_of_populations)
            #     if (self.fitness(self.gen[inx1]) > self.fitness(self.gen[inx2])):
            #         self.gen[num_of_populations - 1 - i] = self.gen[inx1]
            #     else:
            #         self.gen[num_of_populations - 1 - i] = self.gen[inx2]
            #=========#
            # shuffle
            for i in range(0, num_of_populations):
                inx1 = np.random.randint(0, num_of_populations)
                inx2 = np.random.randint(0, num_of_populations)
                while inx2 == inx1:
                    inx2 = np.random.randint(0, num_of_populations)
                if self.fitness(self.gen[inx1]) < int(self.dim / 3):
                    self.gen[inx1] = self.generate_board()
                if self.fitness(self.gen[inx2]) < int(self.dim / 3):
                    self.gen[inx2] = self.generate_board()
                self.gen[inx1], self.gen[inx2] = self.gen[inx2], self.gen[inx1]  
            #=========#
            # crossover
            for i in range(0, int(num_of_populations / 5) * 4):
                # random index
                inx1 = np.random.randint(0, num_of_populations)
                inx2 = np.random.randint(0, num_of_populations)
                while inx2 == inx1:
                    inx2 = np.random.randint(0, num_of_populations)
                # crossover
                self.gen[inx1], self.gen[inx2] = self.crossover(self.gen[inx1], self.gen[inx2])
            #=========#
            # mutate
            for i in range(0, int(num_of_populations/ 10)):
                inx = np.random.randint(0, num_of_populations)
                self.mutate(self.gen[inx])   
            #=========#
            #print and check
            for i in range(0, num_of_populations):
                print(str(self.fitness(self.gen[i])), end=' ')      
                if (self.check(self.gen[i])):
                    #print_board(self.gen[i + 1],self.dim,self.col_constraint,self.row_constraint)
                    ans = copy.deepcopy(self.gen[i])
                    done = True
                    break  
            print('\n') 
            #=========#
            # debug pause       
            # if (generation % 50 == 0):
            #     for i in range(0, num_of_populations):
            #         print_board(self.gen[i],self.dim,self.col_constraint,self.row_constraint)
            #     n = input()

        print_board(ans,self.dim,self.col_constraint,self.row_constraint)
    def mutate(self, state):
        #cur_fitness = self.fitness(state)   
        num_mutate_row = np.random.randint(0, self.dim, np.random.randint(0, self.dim) + 1)
        #print(state)
        for i in range(len(num_mutate_row)):
            np.random.shuffle(state[num_mutate_row[i]])
        #print(state)
            # # finding 1
            # for c in range(0, self.dim):
            #     if (state[id_row][c] == 1 and np.count_nonzero(state[:, c]) > self.col_constraint[c]):
            #         for col_push in range(self.dim):
            #             if (state[id_row][col_push] == 0 and np.count_nonzero(state[:,col_push]) < self.col_constraint[col_push] and np.random.randint(0, 100) < 90): # not enough or max #or self.fitness(state) == 6
            #                 state[id_row][col_push], state[id_row][c] = state[id_row][c], state[id_row][col_push]
            
    def crossover(self,parent1, parent2):
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)
        max_fitness = max(self.fitness(child1), self.fitness(child2))
        for i in range(0, self.dim):
            inx = np.random.randint(0, self.dim)
            child1[inx], child2[inx] = child2[inx], child1[inx]
            if max(self.fitness(child1), self.fitness(child2)) < max_fitness:
                child1[inx], child2[inx] = child2[inx], child1[inx]
            else:
                max_fitness = max(self.fitness(child1), self.fitness(child2))
        return child1, child2
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

    n = int(input())

    # dfs = DFS(gen_object.get_board(), gen_object.get_ship(), gen_object.get_row_constraint(), gen_object.get_col_constraint())
    # dfs.solve()
    # dfs.show()
    # print("Total step search " +str(dfs.get_total_step_search()))

    gen = Genetic(gen_object.get_board(), gen_object.get_ship(), gen_object.get_row_constraint(), gen_object.get_col_constraint())
    gen.solve()
    gen.show()
    print("Total step search " +str(gen.get_total_step_search()))
    
            
                                
                
                
                
                
            