import tkinter as tk  #导入tkinter
import tkinter.messagebox  #导入messagebox模块
from PIL import Image, ImageTk

Main_Width = 600
Bomb_Widsum = 30
Bomb_Higsum = 15
Main_Height = int(Bomb_Higsum*Main_Width/Bomb_Widsum)

Mainwindow = tk.Tk()
redflag_png = Image.open(r'Imgsource\redflag.png')
redflag_img = ImageTk.PhotoImage(redflag_png.resize((int(Main_Width/Bomb_Widsum), int(Main_Height/Bomb_Higsum)), Image.ANTIALIAS))
bomb_png = Image.open(r'Imgsource\bomb.png')
bomb_img = ImageTk.PhotoImage(bomb_png.resize((int(Main_Width/Bomb_Widsum), int(Main_Height/Bomb_Higsum)), Image.ANTIALIAS))

def xFunc1():
    # Mainwindow.update()
    print("当前窗口的宽度为",Mainwindow.winfo_width())
    print("当前窗口的高度为",Mainwindow.winfo_height())
def _init():
    #实例化窗口object
    Mainwindow.title('My Mainwindow')
    Mainwindow.resizable(False,False) #防止用户调整尺寸
    screenWidth,screenHeight = Mainwindow.maxsize()     #获得屏幕宽和高  
    geometryParam = '%dx%d+%d+%d'%(Main_Width+Bomb_Widsum*6, Main_Height+Bomb_Higsum*6, (screenWidth-Main_Width)/2, (screenHeight - Main_Height)/2)
    Mainwindow.geometry(geometryParam)    #设置窗口大小及偏移坐标
    Mainwindow.wm_attributes('-topmost',1)#窗口置顶
    
if __name__ == "__main__":     
    for i in range(Bomb_Higsum):
        for j in range(Bomb_Widsum):
            tk.Button(Mainwindow, width=Main_Width/Bomb_Widsum, height=Main_Height/Bomb_Higsum,image = redflag_img,command = xFunc1).grid(row=i, column=j)
    
    # button1 =tk.Button(Mainwindow, width=int(Main_Width/Bomb_Widsum), height=int(Main_Height/Bomb_Higsum),text=" button")
    # button1.bind("<Button-1>", xFunc1)    # #给按钮控件绑定左键单击事件   
    # button1.pack()
    # 第6步，主窗口循环显示
    Mainwindow.mainloop()
    # 注意，loop因为是循环的意思，window.mainloop就会让window不断的刷新，如果没有mainloop,就是一个静态的window,传入进去的值就不会有循环，mainloop就相当于一个很大的while循环，有个while，每点击一次就会更新一次，所以我们必须要有循环
    # 所有的窗口文件都必须有类似的mainloop函数，mainloop是窗口文件的关键的关键。