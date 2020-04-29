from tkinter import * #导入tkinter
import tkinter.messagebox as Messagebox  #导入messagebox模块
from PIL import Image, ImageTk
import numpy as npy
import matplotlib.pyplot as plt
from threading import Timer
from Astar import A_star
import copy as cp

WIN_W = 200
WIN_H = 200
CNT_W = 3
CNT_H = 3

BLOCK_CLICK = "<Button-1>"
WINDOW_CHANGE = "<Configure>"    

class Puzzle:
    # 初始化对象
    def __init__(self,window):   
        
        self.window = window 
        self.gamelevel = 0
        self.window_size = [WIN_W, WIN_H]
        self.resetup()
        self.window.bind(WINDOW_CHANGE,self.wincallback)
    
    # 重置游戏状态
    def resetup(self):
        cnt_w = CNT_W + self.gamelevel
        cnt_h = CNT_H + self.gamelevel
        SIZE_W = int(WIN_W /cnt_w) 
        SIZE_H = int(WIN_H /cnt_h)  
        self.block_size = [SIZE_W,SIZE_H]
        self.block_count = [cnt_w,cnt_h]
        self.origin_img = None
        self.blank_img = None
        self.blockimg_pho = []
        self.block = dict({})
        self.arrange = npy.zeros(self.block_count[0]*self.block_count [1])
        self.origin_img = Image.open(r'images\level_0.jpg')
        self.blank_img = Image.open(r'images\blank.jpg')
        self.refresh_mainform() 
        self.frame = Frame(self.window)
        self.frame.pack()
        self.resize_modelimg()
        self.arrange = self.generate_arrange(self.block_count[0],self.block_count[1])
        self.init_arr = cp.deepcopy(self.arrange)

        self.generate_block()
        self.refresh_block()
        self.auto_solute()
        self.timer = Timer(5, self.timer_callback)
        self.timer.start()

    def timer_callback(self):
        if(len(self.solution)>0):
            self.arrange = self.solution.pop(0)
            self.refresh_block()
        self.timer.cancel()
        self.timer = Timer(0.4, self.timer_callback)
        self.timer.start()

    def auto_solute(self):
        self.aid_arr = npy.arange(self.block_count[0]*self.block_count[1])
        astar = A_star(self.block_count[0],self.block_count[1],self.init_arr,self.aid_arr)
        self.solution = astar.solve()
        

    # 根据方块数刷新主窗口大小
    def refresh_mainform(self):
        Screen_W,Screen_H = self.window.maxsize()     #获得屏幕宽和高  
        geometryParam = '%dx%d+%d+%d'%(self.window_size[0]+self.block_count[0]*6, self.window_size[0]+self.block_count[0]*6, (Screen_W-self.window_size[0])/2, (Screen_H - self.window_size[1])/2)
        self.window.geometry(geometryParam)    #设置窗口大小及偏移坐标
        self.window.wm_attributes('-topmost',1)#窗口置顶
      
    # 主窗口拖动及缩放回调函数
    def wincallback(self,event):
        #更新窗口大小
        self.window_size = [self.window.winfo_width(),self.window.winfo_height()]
        #更新Block大小
        block_w = int(self.window_size[0]/self.block_count[0] - 6)
        block_h = int(self.window_size[1]/self.block_count[1] - 6)
        self.block_size = [block_w,block_h]
        
        self.resize_modelimg()
        self.changeWidgetsize()
    
    # 模板图切块
    def resize_modelimg(self):
        model_img = self.origin_img.resize((self.window_size[0],self.window_size[1]), Image.ANTIALIAS) 
        blank_img = self.blank_img.resize((self.block_size[0],self.block_size[1]),Image.ANTIALIAS)     
        cnt_w = self.block_count[0]
        cnt_h = self.block_count[1]
        #由于队列直接入队会导致队列无限增长，因此采用判断决定是append入列 or 直接修正值
        for x in range(cnt_h):
            for y in range(cnt_w):
                #第一次启动时，list按序入列
                if(len(self.blockimg_pho) < cnt_w*cnt_h - 1):
                    self.blockimg_pho.append(None) 
                    self.blockimg_pho[x*cnt_w+y] = ImageTk.PhotoImage(model_img.crop((y*self.block_size[0], x*self.block_size[1], (y+1)*self.block_size[0], (x+1)*self.block_size[1])))
                #最后一个放空白块
                elif(len(self.blockimg_pho) == cnt_w*cnt_h - 1):
                    self.blockimg_pho.append(ImageTk.PhotoImage(blank_img))
                #调整窗口大小时，直接更改对应位置的图片
                else:
                    if(x*cnt_w + y < cnt_w*cnt_h - 1):
                        self.blockimg_pho[x*cnt_w+y] = ImageTk.PhotoImage(model_img.crop((y*self.block_size[0], x*self.block_size[1], (y+1)*self.block_size[0], (x+1)*self.block_size[1])))
                    else:
                        self.blockimg_pho[x*cnt_w+y] = ImageTk.PhotoImage(blank_img)
    
    # 改变控件大小
    def changeWidgetsize(self):
        #改变图片按钮大小
        self.refresh_block()
    
    # bind中转站
    def click_adaptor(self, x,y):
        return lambda Button: self.click_image(self.block[x][y],x,y)

    # 交换贴图,真正的图片按钮回调函数
    def click_image(self,block_clicked,clicked_x,clicked_y):
        cnt_w = self.block_count[0]
        cnt_h = self.block_count[1]
        #按下的是空白键时，不操作
        if(block_clicked["id"] == cnt_w*cnt_h - 1):
            return  
        #计算该方块
        top = max(clicked_x - 1,0)
        down = min(clicked_x + 1,cnt_w - 1)
        left = max(clicked_y - 1,0)
        right = min(clicked_y + 1,cnt_h - 1)
        if(self.block[top][clicked_y]["id"] == cnt_w*cnt_h - 1):
            self.arrange[top*cnt_w + clicked_y] = block_clicked["id"]
        elif(self.block[clicked_x][left]["id"] == cnt_w*cnt_h - 1):
            self.arrange[clicked_x*cnt_w + left] = block_clicked["id"]
        elif(self.block[clicked_x][right]["id"] == cnt_w*cnt_h - 1):
            self.arrange[clicked_x*cnt_w + right] = block_clicked["id"]
        elif(self.block[down][clicked_y]["id"] == cnt_w*cnt_h - 1):
            self.arrange[down*cnt_w + clicked_y] = block_clicked["id"]
        else:
            return  
        self.arrange[clicked_x*cnt_w + clicked_y] = cnt_w*cnt_h - 1 
        self.refresh_block()
        if(self.cal_inversenum(self.arrange,self.arrange.size) == 0):
            self.gameover()

    def gameover(self):
        print("Finish!")
        self.gamelevel += 1
        self.timer.cancel()
        self.frame.destroy()
        self.resetup()
        
    
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
    
    # 按钮生成
    def generate_block(self):
        #生成按钮，x为行，y为列
        for x in range(0, self.block_count[0]):
            for y in range(0, self.block_count[1]):
                if y == 0:
                    self.block[x] = {}
                block = {
                    "id": 0,   
                    "button": Button(self.frame, image = self.blockimg_pho[0]),
                }
                block["button"].bind(BLOCK_CLICK, self.click_adaptor(x,y))
                block["button"].grid(row = x, column = y)
                self.block[x][y] = block

    # 刷新图片按钮
    def refresh_block(self):
        cnt_w = self.block_count[0]
        cnt_h = self.block_count[1]
        block_w = self.block_size[0]
        block_h = self.block_size[1]
        for x in range(cnt_h):
            for y in range(cnt_w):
                id = int(self.arrange[x*cnt_w + y])
                self.block[x][y]["id"] = id
                self.block[x][y]["button"].config(image = self.blockimg_pho[id])             
                self.block[x][y]["button"].config(width = block_w,height = block_h)

#主函数
if __name__ == "__main__":
    # 创建TK实例
    window = Tk()
    # 设置窗口名
    window.title("Puzzle Game")
    # 创建游戏实例
    minesweeper = Puzzle(window)
    # 主窗口进程循环
    window.mainloop()