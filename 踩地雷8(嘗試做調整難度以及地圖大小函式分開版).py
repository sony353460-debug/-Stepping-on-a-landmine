import tkinter as tk
from tkinter import messagebox
import random
import pygame #外掛第三方套件


simplex=450
simpley=450

commonx=800
commony=800

difficultx=1500
difficulty=800

bgwidth=0
bgheight=0
key=''
x=0#玩家x座標
y=0#玩家y座標
a=0#一開始隨機取的炸彈x座標
b=0#一開始隨機取的炸彈y座標
minesx=[]#記錄所有取的炸彈x座標
minesy=[]#記錄所有取的炸彈y座標
n=0#隨機取c個炸彈
c=0#紀錄標記起來的地雷數
loadmap=[]#每個格子附近的地雷數
minesmap=[]#地雷地圖位置
bannersmap=[]#插旗地圖位置
latticemap=[]#格子地圖位置
et=[]#Expandterritory
preet=[]#用來儲存已Expandterritory的座標
etmines=0#用來記錄當前位置附近的炸彈數

#角色的操控
def key_down(e):
    global key
    key=e.keysym
    print(key)

def key_up(e):
    global key
    key=''

def player_walk():
    global x,y,et,c
    if key=='w':#向上走
        y-=1
        if y<0:
            y=0
    if key=='s':#向下走
        y+=1
        if y>9:
            y=9
    if key=='a':#向左走
        x-=1
        if x<0:
            x=0
    if key=='d':#向右走
        x+=1
        if x>9:
            x=9
    if key=='e':#挖開格子
        if minesmap[y][x]=='F':
            cvs.delete('tag_lattice'+str(x)+str(y))
            preet.append([x,y])
            latticemap[y][x]=True
            ###判斷玩家所在位置挖開的附近是否有空地
            if loadmap[y][x]==0:
                et.append([x,y])
                print(et)
                Expandterritory0()#如果人物底下是0則執行展地
            if loadmap[y][x]!=0:
                et.append([x,y])
                print(et)
                Expandterritorymines()#如果人物底下是0以外的數字則判斷附近的地雷是否有被標起來，來決定是否展地
        elif minesmap[y][x]=='T':
            pop.play()
            cvs.delete('tag_lattice'+str(x)+str(y))
            cvs.delete('tag_figure')
            messagebox.showinfo('Game over','遊戲結束')
            exit()
    if key=='q':#插旗幟or拔旗幟
        if latticemap[y][x]==False:
            if minesmap[y][x]=='T' or minesmap[y][x]=='F':
                cvs.create_image(x*50,y*50,image=banner,anchor='nw',tag='tag_banner'+str(x)+str(y))
                minesmap[y][x]=minesmap[y][x]+'banner'
            else:
                cvs.delete('tag_banner'+str(x)+str(y))
                minesmap[y][x]=list(minesmap[y][x])[0]
    cvs.coords('tag_figure',x,y)
    for i in range(9):
        for j in range(9):
            if minesmap[i][j]=='Tbanner':
                c+=1
    if c==10:
        messagebox.showinfo('','完成遊戲')
        exit()
    c=0

    form.after(100,player_walk)


#展地函式(格子為0的情況下)
def Expandterritory0():
        if et[0][0]==0:                                            
            if et[0][1]!=0 and et[0][1]!=9:                      
                for i in range(0,3):
                    for j in range(1,3):
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                        latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
                        if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                            et.append([et[0][0]-1+j,et[0][1]-1+i])
            elif et[0][1]==0:                                     
                for i in range(1,3):
                    for j in range(1,3):
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                        latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
                        if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                            et.append([et[0][0]-1+j,et[0][1]-1+i])
            elif et[0][1]==9:                                     
                for i in range(0,2):
                    for j in range(1,3):
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                        latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
                        if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                            et.append([et[0][0]-1+j,et[0][1]-1+i])
        elif et[0][0]==9:                                         
            if et[0][1]!=0 and et[0][1]!=9:                       
                for i in range(0,3):
                    for j in range(0,2):
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                        latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
                        if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                            et.append([et[0][0]-1+j,et[0][1]-1+i])
            elif et[0][1]==0:                                    
                for i in range(1,3):
                    for j in range(0,2):
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                        latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
                        if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                            et.append([et[0][0]-1+j,et[0][1]-1+i])
            elif et[0][1]==9:                                   
                for i in range(0,2):
                    for j in range(0,2):
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                        latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
                        if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                            et.append([et[0][0]-1+j,et[0][1]-1+i])
        elif et[0][1]==0:                                         
            for i in range(1,3):
                for j in range(0,3):
                    cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                    latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
                    if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                        et.append([et[0][0]-1+j,et[0][1]-1+i])
        elif et[0][1]==9:
            for i in range(0,2):
                for j in range(0,3):
                    cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                    latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
                    if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                        et.append([et[0][0]-1+j,et[0][1]-1+i])
        else:                                                     
            for i in range(0,3):
                for j in range(0,3):
                    cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                    latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
                    if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                        et.append([et[0][0]-1+j,et[0][1]-1+i])
        preet.append(et.pop(0))
        if len(et)>0:
            print(et)
            print(preet)
            Expandterritory0()
        


#展地函式(格子附近的地雷被標起來的情況下)
def Expandterritorymines():
    etmines=loadmap[y][x]
    if et[0][0]==0:
        if et[0][1]!=0 and et[0][1]!=9:
            for i in range(0,3):
                for j in range(1,3):
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Tbanner':
                        etmines-=1
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Fbanner':
                        etmines+=9
                    if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                        et.append([et[0][0]-1+j,et[0][1]-1+i])
        elif et[0][1]==0:
            for i in range(1,3):
                for j in range(1,3):
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Tbanner':
                        etmines-=1
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Fbanner':
                        etmines+=9
                    if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                        et.append([et[0][0]-1+j,et[0][1]-1+i])
        elif et[0][1]==9:
            for i in range(0,2):
                for j in range(1,3):
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Tbanner':
                        etmines-=1
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Fbanner':
                        etmines+=9
                    if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                        et.append([et[0][0]-1+j,et[0][1]-1+i])
    elif et[0][0]==9:
        if et[0][1]!=0 and et[0][1]!=9:
            for i in range(0,3):
                for j in range(0,2):
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Tbanner':
                        etmines-=1
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Fbanner':
                        etmines+=9
                    if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                        et.append([et[0][0]-1+j,et[0][1]-1+i])
        elif et[0][1]==0:
            for i in range(1,3):
                for j in range(0,2):
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Tbanner':
                        etmines-=1
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Fbanner':
                        etmines+=9
                    if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                        et.append([et[0][0]-1+j,et[0][1]-1+i])
        elif et[0][1]==9:
            for i in range(0,2):
                for j in range(0,2):
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Tbanner':
                        etmines-=1
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Fbanner':
                        etmines+=9
                    if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                        et.append([et[0][0]-1+j,et[0][1]-1+i])
    elif et[0][1]==0:                                          
        for i in range(1,3):
            for j in range(0,3):
                if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Tbanner':
                    etmines-=1
                if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Fbanner':
                        etmines+=9
                if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                    et.append([et[0][0]-1+j,et[0][1]-1+i])
    elif et[0][1]==9:                                          
        for i in range(0,2):
            for j in range(0,3):
                if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Tbanner':
                    etmines-=1
                if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Fbanner':
                    etmines+=9
                if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                    et.append([et[0][0]-1+j,et[0][1]-1+i])
    else:                                                       
        for i in range(0,3):
            for j in range(0,3):
                if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Tbanner':
                    etmines-=1
                if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Fbanner':
                    etmines+=9
                if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                    et.append([et[0][0]-1+j,et[0][1]-1+i])
    if etmines==0:
        if et[0][0]==0:                                            
            if et[0][1]!=0 and et[0][1]!=9:                      
                for i in range(0,3):
                    for j in range(1,3):
                        if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                            cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                            latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
            elif et[0][1]==0:
                for i in range(1,3):
                    for j in range(1,3):
                        if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                            cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                            latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
            elif et[0][1]==9:
                for i in range(0,2):
                    for j in range(1,3):
                        if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                            cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                            latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
        elif et[0][0]==9:
            if et[0][1]!=0 and et[0][1]!=9:                      
                for i in range(0,3):
                    for j in range(0,2):
                        if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                            cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                            latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
            elif et[0][1]==0:
                for i in range(1,3):
                    for j in range(0,2):
                        if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                            cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                            latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
            elif et[0][1]==9:
                for i in range(0,2):
                    for j in range(0,2):
                        if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                            cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                            latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
        elif et[0][1]==0:
            for i in range(1,3):
                for j in range(0,3):
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                        latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
        elif et[0][1]==9:
            for i in range(0,2):
                for j in range(0,3):
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                        latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
        else:
            for i in range(0,3):
                for j in range(0,3):
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                        latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
        for i in range(len(et)):
            if loadmap[et[0][1]][et[0][0]]==0:
                Expandterritory0()#這邊執行完函式時et串列清空全部轉到preet所以在跳回來時下一行程式找不到et[0](以解決)
                if len(et)==0:
                    break
            else:
                if et[0] not in preet:
                    preet.append(et.pop(0))
                    print(et)
                else:
                    et.pop(0)
                    print(et)
    else:
        for i in range(len(et)): 
            et.pop(0)
    etmines
    


#一開始的遊戲難度設定
def simplebg():   
    global mynumbers,n,x,y
    minesamount=10
    x=500
    y=200
    #把格子以50*50為一格畫線
    for i in range(int(simplex/50)):
        for j in range(int(simpley/50)):
            cvs.create_rectangle(i*50+500,j*50+200,i*50+550,j*50+250,fill='white',outline='black')
    
    for i in range(int(simpley/50)):
        loadmap.append([])
        minesmap.append([])
        bannersmap.append([])
        latticemap.append([])
        for j in range(int(simplex/50)):
            loadmap[i].append(0)
            minesmap[i].append('F')
            bannersmap[i].append(False)
            latticemap[i].append(False)
    print(loadmap)
    print(minesmap)
    print(bannersmap)
    print(latticemap)



    #在地圖上隨機取地雷的座標
    while n<minesamount:
        a=random.randint(0,int(simplex/50-1))
        b=random.randint(0,int(simpley/50-1))
        if a in minesx:
            if b in minesy:
                continue
            else:
                minesx.append(a)
                minesy.append(b)
                n+=1
        else:
            minesx.append(a)
            minesy.append(b)
            n+=1
        print(minesx)
        print(minesy)


    #將為地圖被標記的座標狀態改為True
    for i in range(len(minesx)):
        minesmap[minesy[i]][minesx[i]]='T'
        #做出每個位置的附近的地雷數
        if minesx[i]==0:                                            #第1種可能
            if minesy[i]!=0 and minesy[i]!=simplex/50-1:                       #第1-1種可能
                for j in range(0,3):
                    for k in range(1,3):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
            elif minesy[i]==0:                                      #第1-2種可能
                for j in range(1,3):
                    for k in range(1,3):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
            elif minesy[i]==simplex/50-1:                                      #第1-3種可能
                for j in range(0,2):
                    for k in range(1,3):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
        elif minesx[i]==simplex/50-1:                                          #第2種可能
            if minesy[i]!=0 and minesy[i]!=simplex/50-1:                       #第2-1種可能
                for j in range(0,3):
                    for k in range(0,2):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
            elif minesy[i]==0:                                      #第2-2種可能
                for j in range(1,3):
                    for k in range(0,2):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
            elif minesy[i]==simplex/50-1:                                      #第2-3種可能
                for j in range(0,2):
                    for k in range(0,2):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
        elif minesy[i]==0:                                          #第3種可能
            for j in range(1,3):
                for k in range(0,3):
                    loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
        elif minesy[i]==simplex/50-1:                                          #第4種可能
            for j in range(0,2):
                for k in range(0,3):
                    loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
        else:                                                       #第5種可能
            for j in range(0,3):
                for k in range(0,3):
                    loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1

    #檢查附近地雷數量
    #for i in range(10):
    #   print(loadmap[i])
    #檢查地雷分佈位置
    #for i in range(10):
    #   print(minesmap[i])

    #將格子附近的地雷數標記出來
    for i in range(int(simplex/50)):
        for j in range(int(simpley/50)):
            if loadmap[i][j]!=0:
                mynumbers=cvs.create_text(j*50+525,i*50+225,text=loadmap[i][j],anchor='center')

    #將地雷的圖片放上
    for i in range(minesamount):
        cvs.create_image(minesx[i]*50+500,minesy[i]*50+200,image=mines,anchor='nw',tag='tag_mines')

    #將格子放上畫布
    for i in range(int(simplex/50)):
        for j in range(int(simpley/50)):
            cvs.create_image(j*50+500,i*50+200,image=lattice,anchor='nw',tag='tag_lattice'+str(j)+str(i))
                
    #將玩家放上畫布
    cvs.create_image(x,y,image=figure,anchor='nw',tag='tag_figure')

    #開始按鈕
    btn=tk.Button(cvs,text='遊戲開始',command=startgame,)
    btn.place(x=220,y=530)

    form.bind('<KeyPress>',key_down)
    form.bind('<KeyRelease>',key_up)



def commonbg():   
    global mynumbers,n
    minesamount=40
    #把格子以50*50為一格畫線
    for i in range(int(commonx/50)):
        for j in range(int(commony/50)):
            cvs.create_rectangle(i*50+350,j*50,i*50+400,j*50+50,fill='white',outline='black')

    for i in range(int(commony/50)):
        loadmap.append([])
        minesmap.append([])
        bannersmap.append([])
        latticemap.append([])
        for j in range(int(commonx/50)):
            loadmap[i].append(0)
            minesmap[i].append('F')
            bannersmap[i].append(False)
            latticemap[i].append(False)
    print(loadmap)
    print(minesmap)
    print(bannersmap)
    print(latticemap)



    #在地圖上隨機取地雷的座標
    while n<minesamount:
        a=random.randint(0,int(commonx/50))
        b=random.randint(0,int(commony/50))
        if a in minesx:
            if b in minesy:
                continue
            else:
                minesx.append(a)
                minesy.append(b)
                n+=1
        else:
            minesx.append(a)
            minesy.append(b)
            n+=1
        print(minesx)
        print(minesy)


    #將為地圖被標記的座標狀態改為True
    for i in range(len(minesx)):
        minesmap[minesy[i]][minesx[i]]='T'
        #做出每個位置的附近的地雷數
        if minesx[i]==0:                                            #第1種可能
            if minesy[i]!=0 and minesy[i]!=9:                       #第1-1種可能
                for j in range(0,3):
                    for k in range(1,3):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
            elif minesy[i]==0:                                      #第1-2種可能
                for j in range(1,3):
                    for k in range(1,3):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
            elif minesy[i]==9:                                      #第1-3種可能
                for j in range(0,2):
                    for k in range(1,3):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
        elif minesx[i]==9:                                          #第2種可能
            if minesy[i]!=0 and minesy[i]!=9:                       #第2-1種可能
                for j in range(0,3):
                    for k in range(0,2):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
            elif minesy[i]==0:                                      #第2-2種可能
                for j in range(1,3):
                    for k in range(0,2):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
            elif minesy[i]==9:                                      #第2-3種可能
                for j in range(0,2):
                    for k in range(0,2):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
        elif minesy[i]==0:                                          #第3種可能
            for j in range(1,3):
                for k in range(0,3):
                    loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
        elif minesy[i]==9:                                          #第4種可能
            for j in range(0,2):
                for k in range(0,3):
                    loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
        else:                                                       #第5種可能
            for j in range(0,3):
                for k in range(0,3):
                    loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1

    #檢查附近地雷數量
    #for i in range(10):
    #   print(loadmap[i])
    #檢查地雷分佈位置
    #for i in range(10):
    #   print(minesmap[i])

    #將格子附近的地雷數標記出來
    for i in range(int(commonx/50)):
        for j in range(int(commony/50)):
            if loadmap[i][j]!=0:
                mynumbers=cvs.create_text(25+j*50,25+i*50,text=loadmap[i][j],anchor='center')

    #將地雷的圖片放上
    for i in range(minesamount):
        cvs.create_image(minesx[i]*50,minesy[i]*50,image=mines,anchor='nw',tag='tag_mines')

    #將格子放上畫布
    for i in range(int(commonx/50)):
        for j in range(int(simpley/50)):
            cvs.create_image(j*50,i*50,image=lattice,anchor='nw',tag='tag_lattice'+str(j)+str(i))
                
    #將玩家放上畫布
    cvs.create_image(x,y,image=figure,anchor='nw',tag='tag_figure')

    #開始按鈕
    btn=tk.Button(cvs,text='遊戲開始',command=startgame,)
    btn.place(x=220,y=530)

    form.bind('<KeyPress>',key_down)
    form.bind('<KeyRelease>',key_up)




def difficultbg():   
    global mynumbers,n
    minesamount=99
    #把格子以50*50為一格畫線
    for i in range(int(difficultx/50)):
        for j in range(int(difficulty/50)):
            cvs.create_rectangle(i*50,j*50,i*50+50,j*50+50,fill='white',outline='black')

    for i in range(int(difficulty/50)):
        loadmap.append([])
        minesmap.append([])
        bannersmap.append([])
        latticemap.append([])
        for j in range(int(difficultx/50)):
            loadmap[i].append(0)
            minesmap[i].append('F')
            bannersmap[i].append(False)
            latticemap[i].append(False)
    print(loadmap)
    print(minesmap)
    print(bannersmap)
    print(latticemap)



    #在地圖上隨機取地雷的座標
    while n<minesamount:
        a=random.randint(0,int(difficultx/50))
        b=random.randint(0,int(difficulty/50))
        if a in minesx:
            if b in minesy:
                continue
            else:
                minesx.append(a)
                minesy.append(b)
                n+=1
        else:
            minesx.append(a)
            minesy.append(b)
            n+=1
        print(minesx)
        print(minesy)


    #將為地圖被標記的座標狀態改為True
    for i in range(len(minesx)):
        minesmap[minesy[i]][minesx[i]]='T'
        #做出每個位置的附近的地雷數
        if minesx[i]==0:                                            #第1種可能
            if minesy[i]!=0 and minesy[i]!=9:                       #第1-1種可能
                for j in range(0,3):
                    for k in range(1,3):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
            elif minesy[i]==0:                                      #第1-2種可能
                for j in range(1,3):
                    for k in range(1,3):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
            elif minesy[i]==9:                                      #第1-3種可能
                for j in range(0,2):
                    for k in range(1,3):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
        elif minesx[i]==9:                                          #第2種可能
            if minesy[i]!=0 and minesy[i]!=9:                       #第2-1種可能
                for j in range(0,3):
                    for k in range(0,2):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
            elif minesy[i]==0:                                      #第2-2種可能
                for j in range(1,3):
                    for k in range(0,2):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
            elif minesy[i]==9:                                      #第2-3種可能
                for j in range(0,2):
                    for k in range(0,2):
                        loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
        elif minesy[i]==0:                                          #第3種可能
            for j in range(1,3):
                for k in range(0,3):
                    loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
        elif minesy[i]==9:                                          #第4種可能
            for j in range(0,2):
                for k in range(0,3):
                    loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1
        else:                                                       #第5種可能
            for j in range(0,3):
                for k in range(0,3):
                    loadmap[minesy[i]-1+j][minesx[i]-1+k]+=1

    #檢查附近地雷數量
    #for i in range(10):
    #   print(loadmap[i])
    #檢查地雷分佈位置
    #for i in range(10):
    #   print(minesmap[i])

    #將格子附近的地雷數標記出來
    for i in range(int(difficultx/50)):
        for j in range(int(difficulty/50)):
            if loadmap[i][j]!=0:
                mynumbers=cvs.create_text(25+j*50,25+i*50,text=loadmap[i][j],anchor='center')

    #將地雷的圖片放上
    for i in range(minesamount):
        cvs.create_image(minesx[i]*50,minesy[i]*50,image=mines,anchor='nw',tag='tag_mines')

    #將格子放上畫布
    for i in range(int(difficultx/50)):
        for j in range(int(simpley/50)):
            cvs.create_image(j*50,i*50,image=lattice,anchor='nw',tag='tag_lattice'+str(j)+str(i))
                
    #將玩家放上畫布
    cvs.create_image(x,y,image=figure,anchor='nw',tag='tag_figure')

    #開始按鈕
    btn=tk.Button(cvs,text='遊戲開始',command=startgame,)
    btn.place(x=220,y=530)

    form.bind('<KeyPress>',key_down)
    form.bind('<KeyRelease>',key_up)






#原本錯誤版本              
'''
#展地函式
def Expandterritory():
    print(et)
    if loadmap[et[0][1]][et[0][0]]==0:
        for i in range(0,3):
            for j in range(0,3):
                cvs.delete('tag_lattice'+str(et[0][0]-1+j)+str(et[0][1]-1+i))
                if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [[et[0][0]-1+j][et[0][1]-1+i]] not in et :
                    et.append([et[0][0]-1+j,et[0][1]-1+i])
                print(et)       
        if len(et)>0:
            print
    for i in range(len(et)):
        et.pop()
'''
#開始遊戲
def startgame():
    player_walk()

#一開始的主視窗
form=tk.Tk()
form.geometry('1500x900')
form.title('踩地雷')

#放上畫布
cvs=tk.Canvas(width='1500',height='900',bg='lightgreen')
cvs.pack()

#叫出圖片
figure=tk.PhotoImage(file='./images/figure.png')#玩家(主角)
mines=tk.PhotoImage(file='./images/mines.png')#地雷
lattice=tk.PhotoImage(file='./images/lattice.png')#格子
banner=tk.PhotoImage(file='./images/banner.png')#旗幟

#叫出音效
pygame.mixer.init()#將音效初始化
pop=pygame.mixer.Sound('./music/pop.wav')



btn1=tk.Button(cvs,text='初級',width='10',fg='green',command=simplebg)
btn2=tk.Button(cvs,text='中級',width='10',fg='yellow',command=commonbg)
btn3=tk.Button(cvs,text='高級',width='10',fg='red',command=difficultbg)

btn1.place(x=210,y=580)
btn2.place(x=710,y=580)
btn3.place(x=1210,y=580)




form.mainloop()