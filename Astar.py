import numpy as npy
import copy as cp

class A_star:
    def __init__(self,cnt_w,cnt_h,init_arr,aid_arr):
        self.cnt_w = cnt_w
        self.cnt_h = cnt_h
        # self.arrange = self.generate_arrange( self.cnt_w, self.cnt_h) #排列
        self.arrange = init_arr
        self.print_arrange(self.arrange)
        # self.aid_arr = npy.arange(self.cnt_w*self.cnt_h)
        self.aid_arr = aid_arr

    def solve(self):
        answer = self.main_loop(self.arrange,self.aid_arr)
        for i in range(len(answer)):
            print(">%d"%(i+1))
            self.print_arrange(answer[i])
        return answer

    # Astar主循环
    def main_loop(self,init_arr,aid_arr):
        openList = [] 
        closedList = []
        initState = self.set_afgh(init_arr,parent = None,blank_id = init_arr.size - 1,g = 0, h = self.not_inpos(init_arr,aid_arr))
        initState["parent"] = initState
        openList.append(initState)
        rcount = 0
        while(len(openList) > 0):
            # 获取openList中代价f最小的状态序号，记作当前态
            curState_index = self.getleast_stack(openList)
            # 删除openList中的当前态
            curState = openList.pop(curState_index)
            # 当前态加入closedList
            closedList.append(curState)
            # 生成当前态的子状态
            childArr_List,childBlk_id_List = self.generate_child(curState)
            # 遍历子状态
            for arr_tmp,blk_id in zip(childArr_List,childBlk_id_List):
                # 在closedList中，什么也不做
                if(self.isIn_List(closedList,arr_tmp) is not None):
                    continue
                else:
                    inOpen = self.isIn_List(openList,arr_tmp)
                    # 不在openList中，加入openList
                    if(inOpen is None):
                        openList.append(self.set_afgh(arr_tmp,parent = curState,blank_id = blk_id,g = curState["g"] + 1,  h = self.not_inpos(arr_tmp,aid_arr)))

                    # 在openList中，比较开表中该状态的深度和当前深度
                    elif(inOpen is not None):
                        if(openList[inOpen]["g"] > curState["g"] + 1):
                            openList[inOpen] = self.set_afgh(arr_tmp,parent = curState,blank_id = blk_id,g = curState["g"] + 1,  h = self.not_inpos(arr_tmp,aid_arr))
                statetmp = self.isIn_List(openList,aid_arr)
                if(statetmp is not None):
                    print("Find!")
                    Answer = []
                    tmp = openList[statetmp]
                    count  = 0
                    while((tmp["arr"] == initState["arr"]).all() == False):
                        Answer.insert(0,tmp["arr"])
                        tmp = tmp["parent"]   
                    Answer.insert(0,tmp["arr"])
                    return Answer
                    


    # 产生随机排列
    def generate_arrange(self,cnt_w,cnt_h):
        #获得一组随机排列
        Inverse_num = 0 #逆序数
        arrange = npy.zeros(cnt_w*cnt_h)
        while(Inverse_num <= 1):
            Inverse_num = 0 
            #npy.random.permutation(n) 返回（0,n）的一组随机排列
            arrange[0:cnt_w*cnt_h-1] = npy.random.permutation(cnt_w*cnt_h - 1)
            Inverse_num = self.cal_inversenum(arrange,arrange.size - 1)           
        #最后一位设置为空白格
        arrange[arrange.size - 1] = cnt_w*cnt_h - 1;
        #逆序数为奇数时，拼图无解，所以交换0和1号序号使得排列变为偶排列
        if(Inverse_num%2 == 1):
            tmp = arrange[0]
            arrange[0] = arrange[1]
            arrange[1] = tmp       
        return arrange.astype(npy.int)

    # 计算逆序数
    def cal_inversenum(self,arrange,size):
        inverse_num = 0 
        for i in range(size):
            for j in range(i):
                if (arrange[j] > arrange[i]):
                    inverse_num += 1
        return inverse_num

    # # 返回不在位的拼图数量
    # def not_inpos2(self,arrange,aid_arr):
    #     nums = 0
    #     for i in range(arrange.size):
    #         if(arrange[i] != aid_arr[i] and arrange[i] != arrange.size - 1):
    #             nums += 1
    #     return nums
    
     # 返回不在位的拼图所需步数
    def not_inpos(self,arrange,aid_arr):
        steps = 0
        for i in range(arrange.size):
            if(arrange[i] != aid_arr[i] and arrange[i] != arrange.size - 1):
                aid_col = int(aid_arr[i]/self.cnt_w) #目标行号
                aid_row = aid_arr[i]%self.cnt_w      #目标列号
                cur_col = int(arrange[i]/self.cnt_w) #当前行号
                cur_row = int(arrange[i]/self.cnt_w) #当前列号
                steps += (abs(aid_col- cur_col) + abs(aid_row - cur_row))
        return steps

    # 填充stack, arrange：当前排列状态，blank_id：空白块位置序号，g：深度，h：未在位将牌树
    def set_afgh(self,arrange,parent,blank_id,g,h):
        stack = {
            "parent":parent,
            "arr":arrange,
            "blank_id":blank_id,
            "f":g+h,
            "g":g,  #树深度
            "h":h
        }
        return stack

    # 返回 开表中代价值f最小的arrange序号
    def getleast_stack(self,list):
        index = 0
        f_min = 65535
        for i in range(len(list)):
            if (list[i]["f"] <= f_min):
                f_min = list[i]["f"]
                index = i
        return index
    
    # 生成子状态
    def generate_child(self,curState):
        curArr = cp.deepcopy(curState["arr"])
        blank_col = int(curState["blank_id"]/self.cnt_w) #空白块所在行
        blank_row = curState["blank_id"]%self.cnt_w #空白块所在列
        child_arr = []
        child_blankid = []
        # 生成子状态的排列
        if(blank_row - 1 >= 0):
            arr_tmp = self.exchange_arr(cp.deepcopy(curArr),curState["blank_id"],curState["blank_id"]- 1)          
            if((arr_tmp == curState["parent"]["arr"]).all() == False):
                child_arr.append(arr_tmp)
                child_blankid.append(curState["blank_id"]- 1)
        if(blank_row + 1 < self.cnt_w):
            arr_tmp = self.exchange_arr(cp.deepcopy(curArr),curState["blank_id"],curState["blank_id"]+ 1)
            if((arr_tmp == curState["parent"]["arr"]).all() == False):
                child_arr.append(arr_tmp)
                child_blankid.append(curState["blank_id"]+ 1)
        if(blank_col - 1 >= 0):
            arr_tmp = self.exchange_arr(cp.deepcopy(curArr),curState["blank_id"],curState["blank_id"] - self.cnt_w)
            if((arr_tmp == curState["parent"]["arr"]).all() == False):
                child_arr.append(arr_tmp)
                child_blankid.append(curState["blank_id"] - self.cnt_w)
        if(blank_col + 1 < self.cnt_h):
            arr_tmp = self.exchange_arr(cp.deepcopy(curArr),curState["blank_id"],curState["blank_id"] + self.cnt_w)
            if((arr_tmp == curState["parent"]["arr"]).all() == False):
                child_arr.append(arr_tmp)
                child_blankid.append(curState["blank_id"] + self.cnt_w)
        return child_arr,child_blankid
    
    def print_arrange(self,arr):
        for i in range(self.cnt_h):
            for j in range(self.cnt_w):
                print("%d "%arr[i*self.cnt_w + j],end="")
            print("")
        
    def exchange_arr(self,arrange,init_loc,aid_loc):
        tmp_num = arrange[init_loc]
        arrange[init_loc] = arrange[aid_loc]
        arrange[aid_loc] = tmp_num
        return arrange.astype(npy.int)


    # 判断子状态是否在openList或者closeList
    def isIn_List(self,List,state):
        for i in range (len(List)):
            state_tmp = List[i]
            if((state_tmp["arr"] == state).all() == True):
                return i
        return None

# if __name__ == "__main__":
#     astar = A_star()
    