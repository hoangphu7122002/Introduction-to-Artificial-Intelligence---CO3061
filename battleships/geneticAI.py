from battleships.gen_board import *
import time
import numpy as np
from time import process_time
from battleships.GUI import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import defaultdict

class Genetic:
    def __init__(self, board, ship, row_constraint, col_constraint, dim = 6):
        self.board = np.array(board) #numpy array
        self.prtSolutionBoard = np.array(board)
        self.dim = dim
        self.fix = []
        for row in range(dim):
            for col in range(dim):
                if (board[row][col] == BLOCK):
                    self.fix.append([row, col])
        self.row_constraint = row_constraint
        self.col_constraint = col_constraint
        self.ship = ship
        self.total_step = 0
        self.solution = None
        self.generation = 0
        self.gen = []     
        self.interupt = None
        self.start_time = process_time()
        self.stop_time = 0
        self.population = 50
        if dim == 8:
            self.population = 100
        elif dim == 10:
            self.population = 200
        elif dim == 15:
            self.population = 500
        self.percen_plt = np.zeros(self.dim * 2 + 1)
        self.best_col = []
        self.largest_population = 0
        for i in range(dim):
            self.best_col.append(defaultdict(int))
        self.best_row = []
        for i in range(dim):
            self.best_row.append(defaultdict(int))
    def solve(self):
        num_of_populations = self.population
        # generate(percentage list)
        # min index -> better fitness -> more oppotunity
        percentage = []
        for i in range(self.population):
            percentage.extend([i] * (self.population - i))
        for i in range(num_of_populations):
            self.gen.append(self.generate_board())
        self.gen.sort(key = self.fitness, reverse = True)
        self.generation = 0
        # getting started generation
        # pie chart
        fig, ax = plt.subplots()
        def generate(num):
            try:
                if (self.solution != None):
                    return
            except:
                ax.clear()
                ax.axis('equal')
                mylabels = [str(i) for i in range(self.dim * 2 + 1)]
                ax.set_title("Generation " + str(self.generation) + " | max fitness " + str(self.dim * 2) + "\nSolution found! Close the window to view solution")
                ax.pie(self.percen_plt, labels = mylabels, startangle = 90)
                return
            self.generation += 1
            ax.clear()
            ax.axis('equal')
            ax.set_title("Generation " + str(self.generation) + " | max fitness " + str(self.dim * 2))
            #=========#
            # selection best column and row
            self.best_col.clear()
            self.best_row.clear()
            for i in range(self.dim):
                self.best_col.append(defaultdict(int))
                self.best_row.append(defaultdict(int))
            for i in range(0, num_of_populations):
                # column
                for c in range(0, self.dim):
                    if (np.count_nonzero(self.gen[i][:, c]) == self.col_constraint[c]):
                        self.best_col[c][self.cvt_str(self.gen[i][:, c])] += 1         
                for r in range(0, self.dim):
                    if (np.count_nonzero(self.gen[i][r, :]) == self.row_constraint[r]):
                        self.best_row[r][self.cvt_str(self.gen[i][r, :])] += 1                 
            self.gen.sort(key = self.fitness, reverse = True)
            #=========#
            # crossover
            for i in range(0, int(num_of_populations / 2)):
                # random index
                inx1 = np.random.randint(0, len(percentage))
                inx2 = np.random.randint(0, len(percentage))
                while inx2 == inx1:
                    inx2 = np.random.randint(0, len(percentage))
                inx1 = percentage[inx1]
                inx2 = percentage[inx2]
                # crossover                
                child1, child2 = self.crossover(self.gen[inx1], self.gen[inx2])    
                # mutate            
                if np.random.uniform(0, 1) < 0.1 and self.fitness(self.gen[inx1]) != self.dim * 2:
                    child1 = self.mutate(self.gen[inx1])
                if np.random.uniform(0, 1) < 0.1 and self.fitness(self.gen[inx2]) != self.dim * 2:
                    child2 = self.mutate(self.gen[inx2])
                self.gen.extend([child1, child2])
            ### sort ###
            self.gen.sort(key = self.fitness, reverse = True)
            while (len(self.gen) > self.population):
                self.gen.pop()
            ### check ###
            percen = np.zeros(self.dim * 2 + 1)
            for i in range(0, num_of_populations):                
                tmp = self.fitness(self.gen[i])
                percen[tmp] += 1
                # if (percen[tmp] >= int(self.population * 0.9)) :
                #     # get a half to mutate
                #     for i in range(0, int(self.population * 0.9 * 0.8)):
                #         # some new better column and row will appear and replace the old
                #         self.gen[i] = self.mutate(self.gen[i])
                #     break
                if (tmp == self.dim * 2):
                    # print_board(self.gen[i], self.dim, self.col_constraint, self.row_constraint)
                    if (self.check(self.gen[i])):
                        self.solution = copy.deepcopy(self.gen[i])
                        self.stop_time = process_time() - self.start_time
                    else:
                        self.gen[i] = self.mutate(self.gen[i])
            ### prepare data for pie chart ###
            self.percen_plt = np.array(percen)
            mylabels = [str(i) for i in range(self.dim * 2 + 1)]
            ax.pie(self.percen_plt, labels = mylabels, startangle = 90)
            #=========#
            # debug pause after new 50 generation
            # if (generation % 50 == 0):
            #     for i in range(0, num_of_populations):
            #         print_board(self.gen[i],self.dim,self.col_constraint,self.row_constraint)
            #     n = input() 
        # animation pie chart
        ani = FuncAnimation(fig, generate, frames=range(10000), repeat=False)
        plt.show()
        # Done searching for solution
        try:
            if (self.solution == None):
                print("No solution found yet!")
        except:
            # show solution
            self.show()
            plt.close('all')
            print("===== SOLUTION =====")
            init = Gui(self.prtSolutionBoard,self.dim,self.row_constraint,self.col_constraint)
            init.display_AI(self.generation, self.stop_time)
            vis = np.zeros((self.dim, self.dim))
            for i in range(0, self.dim):
                for j in range(0, self.dim):
                    if (self.solution[i][j] == BLOCK and vis[i][j] == 0):
                        ii = copy.deepcopy(i)
                        jj = copy.deepcopy(j)
                        while (ii in range(0, self.dim) and self.solution[ii][jj] == BLOCK):
                            self.prtSolutionBoard[ii][jj] = BLOCK
                            vis[ii][jj] = 1
                            ii += 1
                        ii = copy.deepcopy(i)
                        jj = copy.deepcopy(j)
                        while (jj in range(0, self.dim) and self.solution[ii][jj] == BLOCK):
                            self.prtSolutionBoard[ii][jj] = BLOCK
                            vis[ii][jj] = 1
                            jj += 1
                        gui_board = Gui(self.prtSolutionBoard,self.dim,self.row_constraint,self.col_constraint)
                        gui_board.display_AI(self.generation, self.stop_time)
            gui_board = Gui(self.prtSolutionBoard,self.dim,self.row_constraint,self.col_constraint)
            gui_board.display_AI(self.generation, self.stop_time, 0)
    def mutate(self, state):
        # stuck case
        # big fitness and big percentage in population
        if (self.fitness(state) >= int(self.dim * 2 * 0.8) and self.percen_plt[self.fitness(state)] >= int(self.population * 0.8)):
            one = []
            for r in range(self.dim):
                for c in range(self.dim):
                    if (state[r][c] == 1):
                        one.append([r, c])
            np.random.shuffle(one)
            for i in range(np.random.randint(0, int(len(one) / 2))):
                rand_row = np.random.randint(0, self.dim)
                rand_col = np.random.randint(0, self.dim)
                while (state[rand_row][rand_col] == 1):
                    rand_row = np.random.randint(0, self.dim)
                    rand_col = np.random.randint(0, self.dim)
                state[rand_row][rand_col] = 1
                state[one[i][0]][one[i][1]] = 0
        balance = 0
        rand = []
        for r in range(self.dim):
            for c in range(self.dim):
                rand.append([r, c])
        np.random.shuffle(rand)
        for i in range(len(rand)):
            r = rand[i][0]
            c = rand[i][1]
            if (state[r][c] == 1 and (np.count_nonzero(state[r, :]) > self.row_constraint[r] or np.count_nonzero(state[:, c]) > self.col_constraint[c])):
                balance += 1
                state[r][c] = 0
            if (state[r][c] == 0 and (np.count_nonzero(state[r, :]) < self.row_constraint[r] or np.count_nonzero(state[:, c]) < self.col_constraint[c])):
                balance -= 1
                state[r][c] = 1
        if (balance == 0):
            return state
        else:
            while (balance > 0):
                rand_row = np.random.randint(0, self.dim)
                rand_col = np.random.randint(0, self.dim)
                while (state[rand_row][rand_col] == 1):
                    rand_row = np.random.randint(0, self.dim)
                    rand_col = np.random.randint(0, self.dim)
                state[rand_row][rand_col] = 1
                balance -= 1
            while (balance < 0):
                rand_row = np.random.randint(0, self.dim)
                rand_col = np.random.randint(0, self.dim)
                while (state[rand_row][rand_col] == 0):
                    rand_row = np.random.randint(0, self.dim)
                    rand_col = np.random.randint(0, self.dim)
                state[rand_row][rand_col] = 0
                balance += 1
            return state
    def crossover(self,parent1, parent2):
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)
        rand = []
        for r in range(self.dim):
            for c in range(self.dim):
                rand.append([r, c])
        np.random.shuffle(rand)
        diff = False
        for i in range(len(rand)):
            r = rand[i][0]
            c = rand[i][1]
            better_col = self.get_better_column(child1[:, c], child2[:, c], c)
            better_row = self.get_better_row(child1[r, :], child2[r, :], r)
            if better_col and better_row and np.random.uniform(0, 1) > 0.6:
                child2[:, c] = child1[:, c]
                child2[r, :] = child1[r, :]
                diff = True
            elif better_col and np.random.uniform(0, 1) > 0.6:
                child2[:, c] = child1[:, c]
                diff = True
            elif better_row and np.random.uniform(0, 1) > 0.6:
                child2[r, :] = child1[r, :]
                diff = True
            else:
                child1[:, c] = child2[:, c]
                child1[r, :] = child2[r, :]
        if not diff:
            child1 = self.mutate(child1)
            child2 = self.mutate(child2)
        return child1, child2
    ####### HELPER FUNCTION ########
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
            cnt += int(np.count_nonzero(state[:, c]) == self.col_constraint[c])
        for r in range(self.dim):
            cnt += int(np.count_nonzero(state[r, :]) == self.row_constraint[r])
        return cnt
    def cvt_str(self, list):
        _str_ = ''
        for i in range(len(list)):
            _str_ += str(int(list[i]))        
        return _str_
    def get_better_column(self, column1, column2, id_col):
        return self.best_col[id_col][self.cvt_str(column1)] > self.best_col[id_col][self.cvt_str(column2)]
    def get_better_row(self, column1, column2, id_row):
        return self.best_col[id_row][self.cvt_str(column1)] > self.best_col[id_row][self.cvt_str(column2)]
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
        vis = np.zeros((self.dim, self.dim))
        type_ship = []
        for r in range(self.dim):
            for c in range(self.dim):
                if (state[r][c] == 0):
                    vis[r][c] = True
                elif state[r][c] == 1 and vis[r][c] == False:
                    run = [r, c]
                    leng = 0
                    ship = []
                    #only 2 direction
                     #go right
                    while (run[1] in range(0, self.dim) and state[run[0]][run[1]] == 1):
                        vis[run[0]][run[1]] = True
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
                        vis[run[0]][run[1]] = True
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
        # self.fix
        for i in range(len(self.fix)):
            if (state[self.fix[i][0]][self.fix[i][1]] != BLOCK):
                return False
        return True
    def show(self):
        try:
            if (self.solution == None):
                print("No solution found yet!")
        except:
            print("Total generations: " + str(self.generation))
            print("Total time search: {:.2f}".format(self.stop_time))
            print("Solution:")
            print_board(self.solution,self.dim,self.col_constraint,self.row_constraint)
    def get_generation(self):
        return self.generation

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
