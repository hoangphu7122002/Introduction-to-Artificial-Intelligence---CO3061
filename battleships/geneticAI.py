from gen_board import *
import time
import numpy as np
from time import process_time

class Genetic:
    def __init__(self, board, ship, row_constraint, col_constraint, dim = 6):
        self.board = np.array(board) #numpy array
        self.dim = dim
        self.row_constraint = row_constraint
        self.col_constraint = col_constraint
        self.ship = ship
        self.total_step = 0
        self.solution = None
        self.generation = 0
        self.gen = []     
        self.interupt = None
        self.begin_time = process_time()
        self.stop_time = 0
    def __search__(self, board):
        pass
    def get_border(self, ship):
        border = []
        for sh in range(0, len(ship)):
            neigh = get_neighbors(self.dim, ship[sh][0], ship[sh][1], 8)
            for ne in range(0, len(neigh)):
                if (not list(neigh[ne]) in ship and not neigh[ne] in border):
                    border.append(neigh[ne])
        return border   
    def check(self, state):
        # not over constraint
        for i in range(self.dim):
            if (np.count_nonzero(state[:,i]) != self.col_constraint[i]):
                return False
            if (np.count_nonzero(state[i,:]) != self.row_constraint[i]):
                return False
        
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
        self.generation = 0
        # getting started generation
        while not done:
            # if (self.solution is not None):# or self.interupt != None
            #     return
            print("Generation " + str(self.generation))
            self.generation += 1
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
                    self.solution = copy.deepcopy(self.gen[i])
                    self.stop_time = process_time() - self.begin_time
                    done = True
                    break  
            print('\n') 
            #=========#
            # debug pause       
            # if (generation % 50 == 0):
            #     for i in range(0, num_of_populations):
            #         print_board(self.gen[i],self.dim,self.col_constraint,self.row_constraint)
            #     n = input()

    def mutate(self, state):
        #cur_fitness = self.fitness(state)   
        num_mutate_row = np.random.randint(0, self.dim, np.random.randint(0, self.dim) + 1)
        #print(state)
        for i in range(len(num_mutate_row)):
            np.random.shuffle(state[num_mutate_row[i]])
            
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
        print("Total generations: " + str(self.generation))
        print("Total time search: {:.2f}".format(self.stop_time))
        print("Solution:")
        print_board(self.solution,self.dim,self.col_constraint,self.row_constraint)
    def get_total_step_search(self):
        return self.total_step

############# debug #############

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

    gen = Genetic(gen_object.get_board(), gen_object.get_ship(), gen_object.get_row_constraint(), gen_object.get_col_constraint())
    gen.solve()
    gen.show()
