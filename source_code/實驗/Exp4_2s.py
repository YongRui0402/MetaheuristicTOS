import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from Board.board import Board
from IDFS_package.bfs import BFS
from IDFS_package.idfs import IDFS,CIDFS,RCIDFS
from GA_package.ga import GA
from ACO_package.aco import ACO,MMAS

import timeit
import json
class Boardstate:
    def __init__(self, boardstring,ball_list,haveMatche):
        # 初始化遊戲盤面
        board = Board()
        board.initialize_board(boardstring)
        self.board = board
        self.boardstring = boardstring
        self.ball_list = ball_list
        self.haveMatche = haveMatche
        self.bestscore = board.cpmpute_best_scroce()
    def print(self):
        print(self.board,self.board)
        
        print(type(self.board),self.board)
        print(type(self.boardstring),self.boardstring)
        print(type(self.ball_list),self.ball_list)
        print(type(self.haveMatche),self.haveMatche)
    def get_boardstring(self):
        return self.boardstring
    def get_ball_list(self):
        return self.ball_list
    def get_haveMatche(self):
        return self.haveMatche
    def get_scroce(self,path,startrow=0,startcol=0):
        self.board.reset_board()
        self.board.make_move(startrow,startcol,path)
        score = self.board.cpmpute_scroce()
        self.board.reset_board()
        return score
    def get_bestscore(self):
        return self.bestscore

class Result:
    def __init__(self, BoardResult,meanScroce,meanScroceR,meanPathlen,meantime):
        self.BoardResult = BoardResult
        self.meanScroce = round(meanScroce,5)
        self.meanScroceR = round(meanScroceR,5)
        self.meantime = round(meantime,5)
        self.meanPathlen = round(meanPathlen,5)

    def savejson(self,filepath="./data.json"):
        dict={
            "BoardResult": self.BoardResult,
            "meanScroce":self.meanScroce,
            "meanScroceR":self.meanScroceR,
            "meanPathlen":self.meanPathlen,
            "meantime":self.meantime
        }
        
        with open(filepath, "w") as file:
            file.write(json.dumps(dict))
        
        
def raedboard(file_path):
    boardstateList = []
    
    with open(file_path, "r") as file:
        line = file.readline()
        while line:
            # print(line)
            
            x=str.split(line.strip(),' ')
            y = [int(i) for i in x[1:-2]]
            boardstate = Boardstate(x[-2],y,x[0]=='true')
            boardstateList.append(boardstate)
            line = file.readline()
    return boardstateList
            
# seed_value = 890402
seed_values = [89,4,2,88,922]
dataset = "文件_評估版面清單/無法消除版面_100"
file_path = f"./整理文件/{dataset}.txt"

boardstateList = raedboard(file_path)
boardstateListNum = len(boardstateList)
testtime = 5
limittime_list = {"RCIDFS":0.9899,"GA":0.9985,"MMAS":0.9899}
limitpathlen = 25


for timei in [1]:

    method = 'RCIDFS'
    parm = [(13,2)]
    print(method)

    # IDFS
    find_max_sol =  3000# 每個步數長探索解的數量上

    print(method)
    for parmi in range(len(parm)):
        MmeanScroce = 0
        MmeanScroceR = 0
        Mmeantime = 0
        MmeanPathlen = 0
        method_str = method
        idfsdeep_max = parm[parmi][0]
        continu_num =  parm[parmi][1]
        print(f"參數{parm[parmi]}")
        for testi in range(testtime):
            start = timeit.default_timer()
            totalScroce = 0
            totalScroceR = 0
            totalPathlen = 0
            data = []

            for i in range(boardstateListNum):
                boardstring = boardstateList[i].get_boardstring()

                rcidfs = RCIDFS(boardstring,find_max_sol,limitpathlen=limitpathlen,limittime=limittime_list[method]+timei,seed_value=seed_values[testi])
                startrow,startcol,best_path = rcidfs.find_path(idfsdeep_max,continu_num)

                
                scroce = round(boardstateList[i].get_scroce(best_path,startrow=startrow,startcol=startcol),5)
                scroceR = round(scroce/boardstateList[i].get_bestscore(),5)
                totalScroce += scroce
                totalScroceR += scroceR 
                totalPathlen += len(best_path)
                data.append([boardstring,best_path,startrow,startcol,scroce])
                # print(boardstring,best_path,scroce)
            end = timeit.default_timer()
            totaltime = end - start
            
            meanScroce = round(totalScroce/boardstateListNum,5)
            meanScroceR = round(totalScroceR/boardstateListNum,5)
            meantime = round(totaltime/boardstateListNum,5)
            meanPathlen = round(totalPathlen/boardstateListNum,5)
            
            MmeanScroce += meanScroce
            MmeanScroceR += meanScroceR
            Mmeantime += meantime
            MmeanPathlen += meanPathlen
            
            result = Result(data,meanScroce,meanScroceR,meanPathlen,meantime)
            savepath = f"./實驗結果/{dataset}/{method_str}_{testi}_time{timei}.json"
            result.savejson(savepath)
            
            print(f"演算法{method_str},平均分數:{meanScroce},平均量化分數:{meanScroceR},平均花費時間:{meantime},平均路進長度:{meanPathlen}")
        MmeanScroce /= testtime
        MmeanScroceR /= testtime
        Mmeantime /= testtime
        MmeanPathlen /= testtime
        print(f"    5次平均,平均分數:{MmeanScroce},平均量化分數:{MmeanScroceR},平均花費時間:{Mmeantime},平均路進長度:{MmeanPathlen}")

    # GA 
    method = 'GA'
    parm = [50]
    generations =  300
    print(method)

    print(method)
    for parmi in range(len(parm)):
        method_str = method
        population_size = parm[parmi]
        MmeanScroce = 0
        MmeanScroceR = 0
        Mmeantime = 0
        MmeanPathlen = 0
        print(f"參數{parm[parmi]}")
        for testi in range(testtime):
            start = timeit.default_timer()
            totalScroce = 0
            totalScroceR = 0
            totalPathlen = 0
            data = []

            for i in range(boardstateListNum):
                boardstring = boardstateList[i].get_boardstring()

                ga = GA(boardstring,limitpathlen=limitpathlen,limittime=limittime_list[method]+timei,seed_value=seed_values[testi])
                startrow,startcol,best_path = ga.find_path(population_size,generations)
                
                
                scroce = round(boardstateList[i].get_scroce(best_path,startrow=startrow,startcol=startcol),5)
                scroceR = round(scroce/boardstateList[i].get_bestscore(),5)
                totalScroce += scroce
                totalScroceR += scroceR 
                totalPathlen += len(best_path)
                data.append([boardstring,best_path,startrow,startcol,scroce])
                # print(boardstring,best_path,scroce)
            end = timeit.default_timer()
            totaltime = end - start
            
            meanScroce = round(totalScroce/boardstateListNum,5)
            meanScroceR = round(totalScroceR/boardstateListNum,5)
            meantime = round(totaltime/boardstateListNum,5)
            meanPathlen = round(totalPathlen/boardstateListNum,5)
            
            MmeanScroce += meanScroce
            MmeanScroceR += meanScroceR
            Mmeantime += meantime
            MmeanPathlen += meanPathlen
            
            result = Result(data,meanScroce,meanScroceR,meanPathlen,meantime)
            savepath = f"./實驗結果/{dataset}/{method_str}_{testi}_time{timei}.json"
            result.savejson(savepath)
            
            print(f"演算法{method_str},平均分數:{meanScroce},平均量化分數:{meanScroceR},平均花費時間:{meantime},平均路進長度:{meanPathlen}")
        MmeanScroce /= testtime
        MmeanScroceR /= testtime
        Mmeantime /= testtime
        MmeanPathlen /= testtime
        print(f"    5次平均,平均分數:{MmeanScroce},平均量化分數:{MmeanScroceR},平均花費時間:{Mmeantime},平均路進長度:{MmeanPathlen}")

    # MMAS 
    method = 'MMAS'
    ants_num = 30
    parm = [9]
    max_iterations = 300
    print(method)


    print(method)
    for parmi in range(len(parm)):
        method_str = method
        update_step = parm[parmi]
        MmeanScroce = 0
        MmeanScroceR = 0
        Mmeantime = 0
        MmeanPathlen = 0
        print(f"參數{parm[parmi]}")
        for testi in range(testtime):
            start = timeit.default_timer()
            totalScroce = 0
            totalScroceR = 0
            totalPathlen = 0
            data = []

            for i in range(boardstateListNum):
                boardstring = boardstateList[i].get_boardstring()

                mmas = MMAS(boardstring,ants_num,update_step,limitpathlen=limitpathlen,limittime=limittime_list[method]+timei,seed_value=seed_values[testi])
                startrow,startcol,best_path = mmas.find_path(max_iterations)
                
                scroce = round(boardstateList[i].get_scroce(best_path,startrow=startrow,startcol=startcol),5)
                scroceR = round(scroce/boardstateList[i].get_bestscore(),5)
                totalScroce += scroce
                totalScroceR += scroceR 
                totalPathlen += len(best_path)
                data.append([boardstring,best_path,startrow,startcol,scroce])
                # print(boardstring,best_path,scroce)
            end = timeit.default_timer()
            totaltime = end - start
            
            meanScroce = round(totalScroce/boardstateListNum,5)
            meanScroceR = round(totalScroceR/boardstateListNum,5)
            meantime = round(totaltime/boardstateListNum,5)
            meanPathlen = round(totalPathlen/boardstateListNum,5)
            
            MmeanScroce += meanScroce
            MmeanScroceR += meanScroceR
            Mmeantime += meantime
            MmeanPathlen += meanPathlen
            
            result = Result(data,meanScroce,meanScroceR,meanPathlen,meantime)
            savepath = f"./實驗結果/{dataset}/{method_str}_{testi}_time{timei}.json"
            result.savejson(savepath)
            
            print(f"演算法{method_str},平均分數:{meanScroce},平均量化分數:{meanScroceR},平均花費時間:{meantime},平均路進長度:{meanPathlen}")
        MmeanScroce /= testtime
        MmeanScroceR /= testtime
        Mmeantime /= testtime
        MmeanPathlen /= testtime
        print(f"    5次平均,平均分數:{MmeanScroce},平均量化分數:{MmeanScroceR},平均花費時間:{Mmeantime},平均路進長度:{MmeanPathlen}")
