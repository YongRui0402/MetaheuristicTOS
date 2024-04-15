import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import numpy as np
import random
from ACO_package.ant import Ant
import timeit

class ACO:
    
    def __init__(self, bead_board_str, n_ants, alpha=1, beta=1, evaporation_rate=0.1,update_step=3,limitpathlen=36,limittime=3,seed_value=-1):
        self.bead_board = np.array(list(bead_board_str)).reshape(5, 6)
        self.bead_board_str = bead_board_str
        self.n_ants = n_ants
        self.pheromone = np.ones((5, 6, 4))
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.ants = [Ant((random.randint(0,4), random.randint(0,5)), self.bead_board_str, self.pheromone, alpha=self.alpha, beta=self.beta) for _ in range(self.n_ants)]
        self.best_path = ""
        self.best_path_startrow = 0
        self.best_path_startcol = 0
        self.best_score = 0
        self.find_sol =  0
        self.update_step = update_step
        self.limitpathlen = limitpathlen
        self.limittime = limittime
        if seed_value !=-1:
            np.random.seed(seed_value)
            random.seed(seed_value)
        
    def make_move(self):
        for ant in self.ants:
            next_move = ant.pick_next_move()
            ant.make_move(next_move)
    
    def make_moves(self, num_moves):
        for ant in self.ants:
            ant.make_moves(num_moves)

    def update_pheromones(self):
        self.pheromone *= (1 - self.evaporation_rate)
        for ant in self.ants:
            for i, move in enumerate(ant.path):
                self.pheromone[ant.current_position[0]][ant.current_position[1]][move] += ant.score
    
    def find_path(self, max_iterations=100):
        now_path_len = 0
        for it in range(max_iterations):
            self.make_moves(self.update_step)
            now_path_len+=self.update_step
            self.update_pheromones()
            for ant in self.ants:
                if ant.score > self.best_score:
                    self.best_path = ant.path.copy()
                    self.best_score = ant.score
            if now_path_len>=self.limitpathlen:
                self.ants = [Ant((random.randint(0,4), random.randint(0,5)), self.bead_board_str, self.pheromone, alpha=self.alpha, beta=self.beta) for _ in range(self.n_ants)]
                now_path_len = 0
        best_path = ''.join(str(x) for x in self.best_path)

        return best_path

class MMAS(ACO):
    def __init__(self, bead_board_str, n_ants, alpha=1, beta=1, evaporation_rate=0.1,update_step=3,limitpathlen=36,limittime=3,seed_value=-1):
        super().__init__(bead_board_str, n_ants, alpha, beta, evaporation_rate,update_step,limitpathlen,limittime,seed_value)
        self.tau_max = 1.0
        self.tau_min = 0.1
    def update_pheromones(self):
        self.pheromone *= (1 - self.evaporation_rate)
        best_ant = max(self.ants, key=lambda ant: ant.score)
        for i, move in enumerate(best_ant.path):
            updated_pheromone = best_ant.score + self.pheromone[best_ant.current_position[0]][best_ant.current_position[1]][move]
            self.pheromone[best_ant.current_position[0]][best_ant.current_position[1]][move] = np.clip(updated_pheromone, self.tau_min, self.tau_max)  # apply limits
    def find_path(self, max_iterations=100):
        stagnation_counter = 0
        max_stagnation = 10
        previous_best_score = -np.inf
        now_path_len = 0
        start = timeit.default_timer()
        best_path = ""
        for it in range(max_iterations):
            self.make_moves(self.update_step)
            now_path_len+=self.update_step
            self.update_pheromones()
            for ant in self.ants:
                if ant.score > self.best_score:
                    self.best_path = ant.path.copy()
                    self.best_score = ant.score
                    self.best_path_startrow = ant.start_position[0]
                    self.best_path_startcol = ant.start_position[1]
                    best_path = ''.join(str(x) for x in self.best_path)

            if self.best_score <= previous_best_score:
                stagnation_counter += 1
            else:
                stagnation_counter = 0
            previous_best_score = self.best_score
            if stagnation_counter >= max_stagnation:
                self.pheromone.fill(self.tau_max)
                stagnation_counter = 0
            if now_path_len>=self.limitpathlen:
                self.ants = [Ant((random.randint(0,4), random.randint(0,5)), self.bead_board_str, self.pheromone, alpha=self.alpha, beta=self.beta) for _ in range(self.n_ants)]
                now_path_len = 0
            if timeit.default_timer() - start > self.limittime:
                return self.best_path_startrow,self.best_path_startcol,best_path
        
        return self.best_path_startrow,self.best_path_startcol,best_path