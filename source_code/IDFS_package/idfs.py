import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Board.board import Board
import random
import timeit

class IDFS:
    def __init__(self, boardstring,find_max_sol=10000):
        board = Board()
        board.initialize_board(boardstring)
        self.board = board
        self.best_path = ""
        self.best_score = 0
        self.find_max_sol =  find_max_sol
        self.find_sol =  0

    def dfs_make_path(self,nowrow,nowcol,nowpath,targetlan):
        if self.find_sol>=self.find_max_sol:
            return
        elif len(nowpath)==targetlan:
            self.find_sol +=1
            self.board.reset_board()
            self.board.make_move(0,0,nowpath)
            score = self.board.cpmpute_scroce()
            if score>self.best_score:
                self.best_score = score
                self.best_path = nowpath
        else:
            if len(nowpath)!=0:
                endstep = nowpath[-1]
            else:
                endstep = "#"
            if nowrow+1<5 and endstep!="2":     # 0 上
                self.dfs_make_path(nowrow+1,nowcol,nowpath+'0',targetlan)
            if nowcol+1<6 and endstep!="3":     # 1 右
                self.dfs_make_path(nowrow,nowcol+1,nowpath+'1',targetlan)
            if nowrow-1>=0 and endstep!="0":    # 2 下
                self.dfs_make_path(nowrow-1,nowcol,nowpath+'2',targetlan)
            if nowcol-1>=0 and endstep!="1":    # 3 左
                self.dfs_make_path(nowrow,nowcol-1,nowpath+'3',targetlan)
    def find_path(self,idfs_deepmax=10):
        for i in range(1,idfs_deepmax):
            self.dfs_make_path(0,0,self.best_path,i)
            self.find_sol = 0
        
        return self.best_path

class CIDFS(IDFS):
    def __init__(self, boardstring,find_max_sol=10000):
        super().__init__(boardstring,find_max_sol)
    
    def find_path(self,idfs_deepmax=10,continu_num=3):
        for _ in range(continu_num):
            tmp_best_path = self.best_path
            for i in range(1,idfs_deepmax):
                self.dfs_make_path(0,0,tmp_best_path,len(tmp_best_path)+i)
                self.find_sol = 0
        return self.best_path

class RCIDFS(CIDFS):
    def __init__(self, boardstring,find_max_sol=10000,limitpathlen=30,limittime=3,seed_value=-1):
        super().__init__(boardstring,find_max_sol)
        self.best_startrow = 0
        self.best_startcol = 0
        self.startrow = 0
        self.startcol = 0
        self.limitpathlen =  limitpathlen
        self.limittime = limittime
        self.starttime = 0
        if seed_value !=-1:
            random.seed(seed_value)
            
    def dfs_make_path(self,nowrow,nowcol,nowpath,targetlan):
        if self.find_sol>=self.find_max_sol:
            if timeit.default_timer() - self.starttime > self.limittime:
                return 
            return
        elif len(nowpath)==targetlan:
            if timeit.default_timer() - self.starttime > self.limittime:
                return 
            self.find_sol +=1
            self.board.reset_board()
            self.board.make_move(self.startrow,self.startcol,nowpath)
            score = self.board.cpmpute_scroce()
            if score>self.best_score:
                self.best_startrow = self.startrow
                self.best_startcol = self.startcol
                self.best_score = score
                self.best_path = nowpath
        else:
            if len(nowpath)!=0:
                endstep = nowpath[-1]
            else:
                endstep = "#"
            numbers = [0, 1, 2, 3]
            endsteps = [2, 3, 0, 1]
            rowadd = [1, 0, -1, 0]
            coladd = [0, 1, 0, -1]
            rcmax = [5, 6, 5, 6]
            random.shuffle(numbers)
            for i in numbers:
                if 0<=nowrow+rowadd[i]<rcmax[i] and 0<=nowcol+coladd[i]<rcmax[i] and endstep!=chr(48+endsteps[i]):
                    self.dfs_make_path(nowrow+rowadd[i],nowcol+coladd[i],nowpath+chr(48+i),targetlan)
    def find_path(self,idfs_deepmax=10,continu_num=3):
        self.starttime = timeit.default_timer()
        for row in range(5):
            for col in range(6):
                self.startrow = row
                self.startcol = col
                tmp_best_path = self.best_path
                for i in range(1,idfs_deepmax):
                    if len(tmp_best_path)+i <= self.limitpathlen:
                        self.dfs_make_path(row,col,tmp_best_path,len(tmp_best_path)+i)
                        self.find_sol = 0
                        if timeit.default_timer() - self.starttime > self.limittime:
                            return self.best_startrow,self.best_startcol,self.best_path
        
        for _ in range(continu_num):
            tmp_best_path = self.best_path
            for i in range(1,idfs_deepmax):
                if len(tmp_best_path)+i <= self.limitpathlen:
                    self.dfs_make_path(self.best_startrow,self.best_startcol,tmp_best_path,len(tmp_best_path)+i)
                    self.find_sol = 0
                    if timeit.default_timer() - self.starttime > self.limittime:
                        return self.best_startrow,self.best_startcol,self.best_path
                    
        return self.best_startrow,self.best_startcol,self.best_path