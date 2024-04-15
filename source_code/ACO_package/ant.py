import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Board.board import Board

import numpy as np
import random

class Ant:
    def __init__(self, start, bead_board_str, pheromone, alpha=1, beta=1):
        self.current_position = start
        self.start_position = start
        self.bead_board = np.array(list(bead_board_str)).reshape(5, 6)
        self.board = Board()
        self.board.initialize_board(bead_board_str)
        self.pheromone = pheromone
        self.alpha = alpha
        self.beta = beta
        self.path = []
        self.score = 0
        
    def get_neighbours(self):
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        neighbours = []
        for i, d in enumerate(directions):
            new_position = (self.current_position[0] + d[0], self.current_position[1] + d[1])
            if 0 <= new_position[0] < self.bead_board.shape[0] and 0 <= new_position[1] < self.bead_board.shape[1]:
                neighbours.append(i)
                
        return neighbours

    def pick_next_move(self):
        neighbours = self.get_neighbours()
        pheromone = np.array([self.pheromone[self.current_position[0]][self.current_position[1]][i] for i in neighbours])
        scores = np.array([self.score_move(n) for n in neighbours])
        probs = pheromone ** self.alpha * scores ** self.beta
        if len(self.path)>0:
            back = (self.path[-1]+2)%4
            probs[neighbours.index(back)] = 0
        probs /= probs.sum()
        move = np.random.choice(neighbours, p=probs)
        
        return move

    def score_move(self, move_direction):
        temp_path = self.path.copy()
        temp_path.append(move_direction)
        temp_path_str=''.join(str(x) for x in temp_path)
        self.board.make_move(self.start_position[0],self.start_position[1],temp_path_str)
        score = self.board.cpmpute_scroce()
        self.board.reset_board()
        
        return score
    
    def update_position(self, current_position, move_direction):
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, right, down, left
        
        return (current_position[0] + directions[move_direction][0],
                current_position[1] + directions[move_direction][1])

    def make_move(self, move_direction):
        path_str=''.join(str(x) for x in self.path)
        self.board.make_move(self.start_position[0],self.start_position[1],path_str)
        self.score = self.board.cpmpute_scroce()
        self.board.reset_board()
        self.path.append(move_direction)
        self.current_position = self.update_position(self.current_position, move_direction)

    def make_moves(self, num_moves):
        for _ in range(num_moves):
            next_move = self.pick_next_move()
            self.path.append(next_move)
            self.current_position = self.update_position(self.current_position, next_move)
        
        path_str=''.join(str(x) for x in self.path)
        self.board.make_move(self.start_position[0],self.start_position[1],path_str)
        self.score = self.board.cpmpute_scroce()
        self.board.reset_board()