t1 = 0
t2 = 0

file_path = "./example.txt"  # 檔案路徑

target_list = [-1,-1,-1,-1,-1,-1]
def cc(total_time,now_time,target_sum,now_sum,upbond):
    global t1,t2,target_list
    t1 += 1
    if now_time == total_time-1 :
        if target_sum-now_sum > upbond:
            return 0
        else:
            target_list[total_time-1]=target_sum-now_sum
            
            result = ' '.join(str(item) for item in target_list)
            with open(file_path, "a") as file:
                boardstring = 'R'*target_list[0]+'G'*target_list[1]+'B'*target_list[2]+'L'*target_list[3]+'D'*target_list[4]+'H'*target_list[5]
                file.write(result+' '+boardstring+'\n')
                
            # print(target_list[:total_time])
            result = list(filter(lambda x: x < 3 and x!=0, target_list[:total_time]))
            if len(result)>0:
                t2 += 1
                # print(result)
            else:
                print(target_list[:total_time])
            
            
                
            target_list[total_time-1]=-1
            return 1
    else:
        sum = 0
        starti = min(upbond,target_sum-now_sum)
        for i in range(starti,-1,-1):
            target_list[now_time]=i
            sum += cc(total_time,now_time+1,target_sum,now_sum+i,i)
            target_list[now_time]=-1
        return sum
    
print(cc(6,0,30,0,30))
print(t1)
print(t2)
