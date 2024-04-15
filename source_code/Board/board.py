import random
from collections import deque
import copy

class Board:
    def __init__(self, rows=5, cols=6):
        self.rows = rows
        self.cols = cols
        self.board = [[None for _ in range(cols)] for _ in range(rows)]
        self.initboard = [[None for _ in range(cols)] for _ in range(rows)]

    def initialize_board(self,initstring=None):
        if initstring is None:
            for row in range(self.rows):
                for col in range(self.cols):
                    self.board[row][col] = self.generate_random_gem()
                    self.initboard[row][col] = self.board[row][col]
        else:
            if len(initstring)==self.rows*self.cols:
                for row in range(self.rows):
                    for col in range(self.cols):
                        self.board[row][col] = initstring[col+row*self.cols]
                        self.initboard[row][col] = self.board[row][col]
            else:
                print("error",len(initstring),self.rows*self.cols)
                
    def reset_board(self):
        self.board = copy.deepcopy(self.initboard)
        
    def boardstring(self):
        boardstring = ""
        for row in range(self.rows):
            for col in range(self.cols):
                boardstring = boardstring+ self.board[row][col]
        return boardstring
        
    def generate_random_gem(self):
        gem_types = ["R", "G", "B", "L", "D", "H"]
        return random.choice(gem_types)

    def display_board(self):
        for row in range(self.rows-1,-1,-1):
            for col in range(self.cols):
                if self.board[row][col] is None:
                    print("-", end=" ")
                else:
                    print(self.board[row][col], end=" ")
            print()  
        print("----------------------------")

    def make_move(self, now_row,now_col,movestring):
        if now_row>=0 and self.rows>now_row and now_col>=0 and self.cols>now_col:
            for item in movestring:
                next_row = now_row
                next_col = now_col
                if item=='0':
                    next_row = now_row + 1
                elif item=='1':
                    next_col = now_col + 1
                elif item=='2':
                    next_row = now_row - 1
                elif item=='3':
                    next_col = now_col - 1
                if next_row>=0 and self.rows>next_row and next_col>=0 and self.cols>next_col:
                    self.board[now_row][now_col],self.board[next_row][next_col] = self.board[next_row][next_col],self.board[now_row][now_col]
                    now_row,now_col = next_row,next_col
                
                    
    def check_matches(self):
        matches = []
        for row in range(self.rows):
            for col in range(self.cols - 2):
                if self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2] != None:
                    matches.append((row, col))
                    matches.append((row, col + 1))
                    matches.append((row, col + 2))
        for col in range(self.cols):
            for row in range(self.rows - 2):
                if self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col] != None:
                    matches.append((row, col))
                    matches.append((row + 1, col))
                    matches.append((row + 2, col))
        return matches

    def remove_matches(self,weight=None):
        weightflag = False
        if weight!=None :
            weightflag = True
        
        combo_count = 0
        ball_count = 0
        ball_score = 0
        ball_weightscore = 0
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        matches = self.check_matches()
        for row, col in matches:
            if not visited[row][col]:
                color = self.board[row][col]
                combo_count += 1
                tmp_ball_count = 1 
                if weightflag:
                    tmp_ball_weightscore = weight[row][col]
                queue = deque([(row, col)])
                visited[row][col] = True

                while queue:
                    current_row, current_col = queue.popleft()
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_row, new_col = current_row + dr, current_col + dc
                        if 0 <= new_row < self.rows and 0 <= new_col < self.cols and not visited[new_row][new_col] and self.board[new_row][new_col] == color and (new_row,new_col) in matches:
                            queue.append((new_row, new_col))
                            visited[new_row][new_col] = True
                            tmp_ball_count += 1
                            if weightflag:
                                tmp_ball_weightscore += weight[new_row][new_col]
                            
                ball_count += tmp_ball_count                            
                ball_score += (1+(tmp_ball_count-3)/4)
                if weightflag:
                    ball_weightscore += (1+(tmp_ball_weightscore-3)/4)
        if not weightflag:
            ball_weightscore = ball_score
            
        for r in range(self.rows):
            for c in range(self.cols):
                if visited[r][c]:
                    self.board[r][c] = None        
        
        return combo_count,ball_count,ball_score,ball_weightscore

    def fill_board(self):
        for col in range(self.cols):
            empty_cells = 0
            for row in range(self.rows):
                if self.board[row][col] is None:
                    empty_cells -= 1
                elif empty_cells < 0:
                    self.board[row + empty_cells][col] = self.board[row][col]
                    self.board[row][col] = None

    def cpmpute_scroce(self):
        weight = [1.25,1.25,1.25,1.25,1.25,1.25],[1.25,1,1,1,1,1.25],[1.25,1,0.75,0.75,1,1.25],[1.25,1,1,1,1,1.25],[1.25,1.25,1.25,1.25,1.25,1.25]
        
        sum_combo_count = 0
        sum_combo_score = 0
        sum_ball_count = 0
        sum_ball_score = 0
        sum_ball_weightscore = 0
        
        matches =  self.check_matches()
        time = 0
        while len(matches) !=0:
            time += 1
            if time == 1:
                combo_count,ball_count,ball_score,ball_weightscore=self.remove_matches(weight)
            else:
                combo_count,ball_count,ball_score,ball_weightscore=self.remove_matches()
            sum_combo_count += combo_count
            sum_ball_count += ball_count
            sum_ball_score += ball_score
            sum_ball_weightscore += ball_weightscore
            self.fill_board()
            matches =  self.check_matches()
        scroce_loss = self.cpmpute_scroce_loss()
        maybe_combo_score,maybe_ball_score = self.cpmpute_scroce_loss2()
        if sum_combo_count>0:
            sum_combo_score = 1+(sum_combo_count-1)/4
        
        # 消除的分數
        cost_part1 = sum_combo_score*sum_ball_weightscore
        # 可消除但未消除的分數
        cost_part2 = -1*maybe_combo_score*maybe_ball_score + 32.5
        # 最後剩下版面的整潔度
        cost_part3 = scroce_loss
        # print(f"評價函數:{cost_part1+cost_part2+cost_part3}")
        return (cost_part1+cost_part2+cost_part3)

    def cpmpute_scroce_loss(self):  # 評估剩餘版面相連價值
        ball_score = 0
        ball_count = 0
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        
        for col in range(self.cols):
            for row in range(self.rows):
                if not visited[row][col] :
                    visited[row][col] = True
                    if self.board[row][col]!=None:
                        color = self.board[row][col]
                        queue = deque([(row, col)])
                        tmp_ball_count = 1
                        while queue:
                            current_row, current_col = queue.popleft()
                            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                new_row, new_col = current_row + dr, current_col + dc
                                if 0 <= new_row < self.rows and 0 <= new_col < self.cols and not visited[new_row][new_col] and self.board[new_row][new_col] == color:
                                    queue.append((new_row, new_col))
                                    visited[new_row][new_col] = True
                                    tmp_ball_count += 1
                        ball_count += tmp_ball_count
                        ball_score += tmp_ball_count**2/9
        if ball_count==0:
            return 0
        else:
            return ball_score/ball_count
    def cpmpute_scroce_loss2(self): # 評估剩餘版面潛力價值
        dic={}
        ball_count = 0
        combo_count = 0
        ball_score = 0
        combo_score = 0
        for col in range(self.cols):
            for row in range(self.rows):
                if self.board[row][col]!=None:
                    if self.board[row][col] in dic:
                        dic[self.board[row][col]] += 1
                    else:
                        dic[self.board[row][col]] = 1   
        for item in dic:
            if dic[item]>=3:
                ball_count += dic[item]
                combo_count += dic[item]//3
                if dic[item]%3==0:
                    ball_score += dic[item]//3
                else:
                    if dic[item]//3>=1:
                        tmp_combo = dic[item]//3-1
                        ball_score += tmp_combo
                        ball_score += (1+(dic[item]-tmp_combo*3-3)/4)
                    else:
                        ball_score += (dic[item]-(dic[item]//3)*3)**2/9
                        
        if combo_count>0:
            combo_score = 1+(combo_count-1)/4
        return combo_score,ball_score
    def cpmpute_best_scroce(self):# 評估版面最大分數
        dic={}
        ball_count = 0
        combo_count = 0
        ball_score = 0
        combo_score = 0
        cant_drop_ball_score = 0
        for col in range(self.cols):
            for row in range(self.rows):
                if self.board[row][col]!=None:
                    if self.board[row][col] in dic:
                        dic[self.board[row][col]] += 1
                    else:
                        dic[self.board[row][col]] = 1
        for item in dic:
            if dic[item]>=3:
                ball_count += dic[item]
                combo_count += dic[item]//3
                if dic[item]//3>6:
                    combo_count -= dic[item]//3-6
                    
                if dic[item]%3==0:
                    tmp_combo = dic[item]//3-1
                    ball_score += tmp_combo
                    ball_score += (1+(dic[item]-tmp_combo*3-3)/4)
                else:
                    if dic[item]//3>=1:
                        tmp_combo = dic[item]//3-1
                        ball_score += tmp_combo
                        ball_score += (1+(dic[item]-tmp_combo*3-3)/4)
                    else:
                        cant_drop_ball_score += (dic[item]-(dic[item]//3)*3)**2/9
        if combo_count>0:
            combo_score = 1+(combo_count-1)/4
        cost_part1 = combo_score*ball_score
        cost_part2 = -0 + 32.5
        cost_part3 = cant_drop_ball_score
        return (cost_part1+cost_part2+cost_part3)