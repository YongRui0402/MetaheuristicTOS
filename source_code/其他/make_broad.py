import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from Board.board import Board

import random

file_path = "簡化所有版面清單.txt"  # 檔案路徑
board_list = []
board_ball_list = []
with open(file_path, "r") as file:
    line = file.readline()
    while line:
        # print(line)
        x=str.split(line.strip(),' ')
        board_list.append(x[-1])
        board_ball_list.append(' '.join(x[:-1]))
        line = file.readline()

file_path = "./無法消除版面.txt"
# print(board_list)
board = Board()
for i in range(len(board_list)):
    NoMatchesFlag = False
    for j in range(10000):
        characters = list(board_list[i])
        random.shuffle(characters)
        shuffled_string = ''.join(characters)
        
        board.initialize_board(shuffled_string)
        # print(board.check_matches())
        
        if len(board.check_matches())==0:
            print(shuffled_string)
            NoMatchesFlag = True
            break
    print(NoMatchesFlag,j)
    
    flag = "true"
    if not NoMatchesFlag:
        shuffled_string = board_list[i]
        flag = "false"
    with open(file_path, "a") as file:
        file.write(flag+' '+board_ball_list[i]+' '+shuffled_string+'\n')
