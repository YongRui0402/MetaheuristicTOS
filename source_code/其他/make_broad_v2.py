import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from Board.board import Board

import random
file_path = "C:/Users/GuoRui/Desktop/metaheuristic_project/整理文件/無法消除版面_1206.txt"  # 檔案路徑
find_board_list = []
board_list = []
board_ball_list = []
with open(file_path, "r") as file:
    line = file.readline()
    while line:
        # print(line)
        x=str.split(line.strip(),' ')
        board_list.append(x[-1])
        find_board_list.append(x[0])
        board_ball_list.append(' '.join(x[1:-1]))
        line = file.readline()

file_path = "./無法消除版面v2.txt"
# print(board_list)
board = Board()

    
for i in range(len(board_list)): #,len(board_list)
    if find_board_list[i]=="false":
        NoMatchesFlag = False
        
        characters = list(board_list[i])
        for j in range(1000):
            shuffled_string = ''.join(characters)
            board.initialize_board(shuffled_string)
            # print(board.check_matches())
            
            if len(board.check_matches())==0:
                print(shuffled_string)
                NoMatchesFlag = True
                break
            
            random.shuffle(characters)
        print(NoMatchesFlag,j)
    
        # flag = "true"
        # if not NoMatchesFlag:
        #     shuffled_string = board_list[i]
        #     flag = "false"
        flag = "false"
        with open(file_path, "a") as file:
            file.write(flag+' '+board_ball_list[i]+' '+shuffled_string+' '+ str(board.cpmpute_best_scroce())+'\n')
    else:
        board = Board()
        board.initialize_board(board_list[i])
        with open(file_path, "a") as file:
            file.write(find_board_list[i]+' '+board_ball_list[i]+' '+board_list[i]+' '+ str(board.cpmpute_best_scroce())+'\n')
            

# samples = ['RR*RR*RR*RR*RR*RR*RR*RR*RR*RR*','R*RR*RR*RR*RR*RR*RR*RR*RR*RR*R','*RR*RR*RR*RR*RR*RR*RR*RR*RR*RR']

# for i in range(83,113):
    
#     y=str.split(board_ball_list[i],' ')
#     y = [int(x) for x in y[1:]]
#     addstr='G'*y[0]+'B'*y[1]+'L'*y[2]+'D'*y[3]+'H'*y[4]
#     addstrlist = list(addstr)
#     random.shuffle(addstrlist)
#     shuffled_string = ''.join(addstrlist)
    
#     result = ""
#     addstrid = 0
#     sample = random.choice(samples)
#     for j in range(len(sample)):
#         if sample[j]=='*':
#             result = result + shuffled_string[addstrid]
#             addstrid +=1
#         else:
#             result = result + sample[j]
#     result2 = ""
#     for x in range(5):
#         for y in range(6):
#             result2 = result2+result[x+y*5]
        
#     print(y,addstr,result,result2)
#     flag = "false"
#     with open(file_path, "a") as file:
#         file.write(flag+' '+board_ball_list[i]+' '+result2+'\n')