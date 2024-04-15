import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Board.board import Board

import random

class BFS:
    def __init__(self, boardstring,start=0,findnum=100):
        board = Board()
        board.initialize_board(boardstring)
        self.board = board
        self.best_path = ""
        self.best_score = 0
        self.findnum = findnum
        self.start = start
        
    def yield_make_path(self):
        path_list = []
        start = self.start
        if start<=0:
            path_list.append(0)
            
            yield ''.join(str(x) for x in path_list)
        else:
            while start>0:
                tmpi = start%4
                path_list.append(tmpi)
                start = start//4
                
            yield ''.join(str(x) for x in path_list)
        while True:
            path_list[0] += 1
            checkid = 0
            while path_list[checkid]>=4:
                path_list[checkid]=0
                if checkid+1>=len(path_list):
                    path_list.append(1)
                else:
                    path_list[checkid+1]+=1
                checkid+=1
                
            yield ''.join(str(x) for x in path_list)
    
    def find_path(self):
        sol=self.yield_make_path()
        for _ in range(self.findnum):
        
            path=next(sol)
            self.board.reset_board()
            self.board.make_move(0,0,path)
            score = self.board.cpmpute_scroce()
            if score>self.best_score:
                self.best_score = score
                self.best_path = path
        
        return self.best_path