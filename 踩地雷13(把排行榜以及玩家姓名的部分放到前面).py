import tkinter as tk
from tkinter import messagebox
import random
import pygame #外掛第三方套件

model=0#1為簡單，2為普通，3為困難
modelx=0#各難度地圖串列邊界的x座標
modely=0#各難度地圖串列邊界的y座標
initialx=0#各難度地圖的初始x座標
initialy=0#各難度地圖的初始y座標
bgwidth=0#畫布寬度
bgheight=0#畫布高度
count=0#遊戲時間
counts=False#遊戲結束時讓時間也停止的變數
key=''
x=0#玩家x座標
y=0#玩家y座標
minesamount=0#個難度地圖的地雷數
a=0#一開始隨機取的炸彈x座標
b=0#一開始隨機取的炸彈y座標
minesxy=[]#記錄所有取的炸彈x,y座標
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
    global x,y,et,c,counts
    if key=='w':#向上走
        y-=1
        if y<initialy:
            y=initialy
    if key=='s':#向下走
        y+=1
        if y>initialy+modely-1:
            y=initialy+modely-1
    if key=='a':#向左走
        x-=1
        if x<initialx:
            x=initialx
    if key=='d':#向右走
        x+=1
        if x>initialx+modelx-1:
            x=initialx+modelx-1
    if key=='e':#挖開格子
        if minesmap[y-initialy][x-initialx]=='F':
            cvs.delete('tag_lattice'+str(x-initialx)+','+str(y-initialy))
            #preet.append([x-initialx,y-initialy])
            latticemap[y-initialy][x-initialx]=True
            ###判斷玩家所在位置挖開的附近是否有空地
            if loadmap[y-initialy][x-initialx]==0:
                et.append([x-initialx,y-initialy])
                print(et)
                Expandterritory0()#如果人物底下是0則執行展地
            if loadmap[y-initialy][x-initialx]!=0:
                et.append([x-initialx,y-initialy])
                print(et)
                Expandterritorymines()#如果人物底下是0以外的數字則判斷附近的地雷是否有被標起來，來決定是否展地
        elif minesmap[y-initialy][x-initialx]=='T':
            pop.play()
            cvs.delete('tag_lattice'+str(x-initialx)+','+str(y-initialy))
            cvs.delete('tag_figure')
            messagebox.showinfo('Game over','遊戲結束')
            counts=True
            exit()
    if key=='q':#插旗幟or拔旗幟
        if latticemap[y-initialy][x-initialx]==False:
            if minesmap[y-initialy][x-initialx]=='T' or minesmap[y-initialy][x-initialx]=='F':
                cvs.create_image(x*50,y*50,image=banner,anchor='nw',tag='tag_banner'+str(x-initialx)+str(y-initialy))
                minesmap[y-initialy][x-initialx]=minesmap[y-initialy][x-initialx]+'banner'
            else:
                cvs.delete('tag_banner'+str(x-initialx)+str(y-initialy))
                minesmap[y-initialy][x-initialx]=list(minesmap[y-initialy][x-initialx])[0]
    else:
        cvs.coords('tag_figure',x*50,y*50)
    for i in range(modely):
        for j in range(modelx):
            if minesmap[i][j]=='Tbanner':
                c+=1
    if c==minesamount:
        counts=True
        scoring()
        messagebox.showinfo('','完成遊戲')
        exit()
    c=0

    form.after(100,player_walk)


#展地函式(格子為0的情況下)
def Expandterritory0():
        if et[0][0]==0:                                            
            if et[0][1]!=0 and et[0][1]!=modely-1:                      
                for i in range(0,3):
                    for j in range(1,3):
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
                        latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
                        if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                            et.append([et[0][0]-1+j,et[0][1]-1+i])
            elif et[0][1]==0:                                     
                for i in range(1,3):
                    for j in range(1,3):
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
                        latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
                        if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                            et.append([et[0][0]-1+j,et[0][1]-1+i])
            elif et[0][1]==modely-1:                                     
                for i in range(0,2):
                    for j in range(1,3):
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
                        latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
                        if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                            et.append([et[0][0]-1+j,et[0][1]-1+i])
        elif et[0][0]==modelx-1:                                         
            if et[0][1]!=0 and et[0][1]!=modely-1:                       
                for i in range(0,3):
                    for j in range(0,2):
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
                        latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
                        if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                            et.append([et[0][0]-1+j,et[0][1]-1+i])
            elif et[0][1]==0:                                    
                for i in range(1,3):
                    for j in range(0,2):
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
                        latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
                        if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                            et.append([et[0][0]-1+j,et[0][1]-1+i])
            elif et[0][1]==modely-1:                                   
                for i in range(0,2):
                    for j in range(0,2):
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
                        latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
                        if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                            et.append([et[0][0]-1+j,et[0][1]-1+i])
        elif et[0][1]==0:                                         
            for i in range(1,3):
                for j in range(0,3):
                    cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
                    latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
                    if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                        et.append([et[0][0]-1+j,et[0][1]-1+i])
        elif et[0][1]==modely-1:
            for i in range(0,2):
                for j in range(0,3):
                    cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
                    latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
                    if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                        et.append([et[0][0]-1+j,et[0][1]-1+i])
        else:                                                     
            for i in range(0,3):
                for j in range(0,3):
                    cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
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
    etmines=loadmap[y-initialy][x-initialx]
    if et[0][0]==0:
        if et[0][1]!=0 and et[0][1]!=modely-1:
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
        elif et[0][1]==modely-1:
            for i in range(0,2):
                for j in range(1,3):
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Tbanner':
                        etmines-=1
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]=='Fbanner':
                        etmines+=9
                    if loadmap[et[0][1]-1+i][et[0][0]-1+j]==0 and [et[0][0]-1+j,et[0][1]-1+i] not in preet and [et[0][0]-1+j,et[0][1]-1+i] not in et:
                        et.append([et[0][0]-1+j,et[0][1]-1+i])
    elif et[0][0]==modelx-1:
        if et[0][1]!=0 and et[0][1]!=modely-1:
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
        elif et[0][1]==modely-1:
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
    elif et[0][1]==modely-1:                                          
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
            if et[0][1]!=0 and et[0][1]!=modely-1:                      
                for i in range(0,3):
                    for j in range(1,3):
                        if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                            cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
                            latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
            elif et[0][1]==0:
                for i in range(1,3):
                    for j in range(1,3):
                        if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                            cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
                            latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
            elif et[0][1]==modely-1:
                for i in range(0,2):
                    for j in range(1,3):
                        if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                            cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
                            latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
        elif et[0][0]==modelx-1:
            if et[0][1]!=modely-1 and et[0][1]!=modely-1:                      
                for i in range(0,3):
                    for j in range(0,2):
                        if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                            cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
                            latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
            elif et[0][1]==0:
                for i in range(1,3):
                    for j in range(0,2):
                        if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                            cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
                            latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
            elif et[0][1]==modely-1:
                for i in range(0,2):
                    for j in range(0,2):
                        if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                            cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
                            latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
        elif et[0][1]==0:
            for i in range(1,3):
                for j in range(0,3):
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
                        latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
        elif et[0][1]==modely-1:
            for i in range(0,2):
                for j in range(0,3):
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
                        latticemap[et[0][1]-1+i][et[0][0]-1+j]=True
        else:
            for i in range(0,3):
                for j in range(0,3):
                    if minesmap[et[0][1]-1+i][et[0][0]-1+j]!='Tbanner':
                        cvs.delete('tag_lattice'+str(et[0][0]-1+j)+','+str(et[0][1]-1+i))
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
#簡單模式
def simplebg():   
    global mynumbers,n,x,y,modelx,modely,model,borderx,bordery,initialx,initialy,minesamount
    model=1
    minesamount=10
    x=11
    y=4
    modelx=9
    modely=9
    initialx=11
    initialy=4
    #把格子以50*50為一格畫線
    for i in range(int(modelx)):
        for j in range(int(modely)):
            cvs.create_rectangle(i*50+550,j*50+200,i*50+600,j*50+250,fill='white',outline='black')
    
    for i in range(int(modely)):
        loadmap.append([])
        minesmap.append([])
        bannersmap.append([])
        latticemap.append([])
        for j in range(int(modelx)):
            loadmap[i].append(0)
            minesmap[i].append('F')
            bannersmap[i].append(False)
            latticemap[i].append(False)

    #在地圖上隨機取地雷的座標
    while n<minesamount:
        a=[random.randint(0,int(modelx)-1),random.randint(0,int(modely)-1)]
        if a in minesxy:
            continue
        minesxy.append(a)
        n+=1
        print(minesxy)

    #將為地圖被標記的座標狀態改為True
    for i in range(len(minesxy)):
        minesmap[minesxy[i][1]][minesxy[i][0]]='T'
        #做出每個位置的附近的地雷數
        if minesxy[i][0]==0:                                            #第1種可能
            if minesxy[i][1]!=0 and minesxy[i][1]!=modely-1:                       #第1-1種可能
                for j in range(0,3):
                    for k in range(1,3):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
            elif minesxy[i][1]==0:                                      #第1-2種可能
                for j in range(1,3):
                    for k in range(1,3):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
            elif minesxy[i][1]==modely-1:                                      #第1-3種可能
                for j in range(0,2):
                    for k in range(1,3):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
        elif minesxy[i][0]==modelx-1:                                          #第2種可能
            if minesxy[i][1]!=0 and minesxy[i][1]!=modelx-1:                       #第2-1種可能
                for j in range(0,3):
                    for k in range(0,2):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
            elif minesxy[i][1]==0:                                      #第2-2種可能
                for j in range(1,3):
                    for k in range(0,2):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
            elif minesxy[i][1]==modelx-1:                                      #第2-3種可能
                for j in range(0,2):
                    for k in range(0,2):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
        elif minesxy[i][1]==0:                                          #第3種可能
            for j in range(1,3):
                for k in range(0,3):
                    loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
        elif minesxy[i][1]==modelx-1:                                          #第4種可能
            for j in range(0,2):
                for k in range(0,3):
                    loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
        else:                                                       #第5種可能
            for j in range(0,3):
                for k in range(0,3):
                    loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1

    #檢查附近地雷數量
    #for i in range(10):
    #   print(loadmap[i])
    #檢查地雷分佈位置
    #for i in range(modelx):
    #   print(minesmap[i])


    #將格子附近的地雷數標記出來
    for i in range(int(modely)):
        for j in range(int(modelx)):
            if loadmap[i][j]!=0:
                mynumbers=cvs.create_text(j*50+575,i*50+225,text=loadmap[i][j],anchor='center')

    #將地雷的圖片放上
    for i in range(minesamount):
        cvs.create_image(minesxy[i][0]*50+550,minesxy[i][1]*50+200,image=mines,anchor='nw',tag='tag_mines')

    #將格子放上畫布
    for i in range(int(modely)):
        for j in range(int(modelx)):
            cvs.create_image(j*50+550,i*50+200,image=lattice,anchor='nw',tag='tag_lattice'+str(j)+','+str(i))
                
    #將玩家放上畫布
    cvs.create_image(x*50,y*50,image=figure,anchor='nw',tag='tag_figure')


    #刪除個難度的檢視圖
    cvs.delete('tag_simple')
    cvs.delete('tag_common')
    cvs.delete('tag_difficult')

    #刪除選擇模式按鈕
    btn1.destroy()
    btn2.destroy()
    btn3.destroy()

    lab1.destroy() 

    #開始按鈕
    btn=tk.Button(cvs,text='遊戲開始',command=startgame)
    btn.place(x=730,y=40)

    form.bind('<KeyPress>',key_down)
    form.bind('<KeyRelease>',key_up)


#普通模式
def commonbg():   
    global mynumbers,n,x,y,modelx,modely,model,borderx,bordery,initialx,initialy,minesamount
    model=2
    minesamount=40
    x=7
    y=8
    modelx=16
    modely=16
    borderx=23
    bordery=24
    initialx=7
    initialy=2
    #把格子以50*50為一格畫線
    for i in range(int(modelx)):
        for j in range(int(modely)):
            cvs.create_rectangle(i*50+350,j*50+100,i*50+400,j*50+150,fill='white',outline='black')

    for i in range(int(modely)):
        loadmap.append([])
        minesmap.append([])
        bannersmap.append([])
        latticemap.append([])
        for j in range(int(modelx)):
            loadmap[i].append(0)
            minesmap[i].append('F')
            bannersmap[i].append(False)
            latticemap[i].append(False)


    #在地圖上隨機取地雷的座標
    while n<minesamount:
        a=[random.randint(0,int(modelx)-1),random.randint(0,int(modely)-1)]
        if a in minesxy:
            continue
        minesxy.append(a)
        n+=1
        print(minesxy)

    #將為地圖被標記的座標狀態改為True
    for i in range(len(minesxy)):
        minesmap[minesxy[i][1]][minesxy[i][0]]='T'
        #做出每個位置的附近的地雷數
        if minesxy[i][0]==0:                                            #第1種可能
            if minesxy[i][1]!=0 and minesxy[i][1]!=modely-1:                       #第1-1種可能
                for j in range(0,3):
                    for k in range(1,3):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
            elif minesxy[i][1]==0:                                      #第1-2種可能
                for j in range(1,3):
                    for k in range(1,3):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
            elif minesxy[i][1]==modely-1:                                      #第1-3種可能
                for j in range(0,2):
                    for k in range(1,3):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
        elif minesxy[i][0]==modelx-1:                                          #第2種可能
            if minesxy[i][1]!=0 and minesxy[i][1]!=modely-1:                       #第2-1種可能
                for j in range(0,3):
                    for k in range(0,2):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
            elif minesxy[i][1]==0:                                      #第2-2種可能
                for j in range(1,3):
                    for k in range(0,2):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
            elif minesxy[i][1]==modely-1:                                      #第2-3種可能
                for j in range(0,2):
                    for k in range(0,2):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
        elif minesxy[i][1]==0:                                          #第3種可能
            for j in range(1,3):
                for k in range(0,3):
                    loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
        elif minesxy[i][1]==modely-1:                                          #第4種可能
            for j in range(0,2):
                for k in range(0,3):
                    loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
        else:                                                       #第5種可能
            for j in range(0,3):
                for k in range(0,3):
                    loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1

    #檢查附近地雷數量
    #for i in range(10):
    #   print(loadmap[i])
    #檢查地雷分佈位置
    #for i in range(10):
    #   print(minesmap[i])

    #將格子附近的地雷數標記出來
    for i in range(int(modely)):
        for j in range(int(modelx)):
            if loadmap[i][j]!=0:
                mynumbers=cvs.create_text(j*50+375,i*50+125,text=loadmap[i][j],anchor='center')

    #將地雷的圖片放上
    for i in range(minesamount):
        cvs.create_image(minesxy[i][0]*50+350,minesxy[i][1]*50+100,image=mines,anchor='nw',tag='tag_mines')

    #將格子放上畫布
    for i in range(int(modely)):
        for j in range(int(modelx)):
            cvs.create_image(j*50+350,i*50+100,image=lattice,anchor='nw',tag='tag_lattice'+str(j)+','+str(i))
                
    #將玩家放上畫布
    cvs.create_image(x*50,y*50,image=figure,anchor='nw',tag='tag_figure')

    #刪除個難度的檢視圖
    cvs.delete('tag_simple')
    cvs.delete('tag_common')
    cvs.delete('tag_difficult')

    #刪除選擇模式按鈕
    btn1.destroy()
    btn2.destroy()
    btn3.destroy()

    lab1.destroy()    

    #開始按鈕
    btn=tk.Button(cvs,text='遊戲開始',command=startgame,)
    btn.place(x=730,y=40)

    form.bind('<KeyPress>',key_down)
    form.bind('<KeyRelease>',key_up)



#困難模式
def difficultbg():   
    global mynumbers,n,x,y,modelx,modely,model,borderx,bordery,initialx,initialy,minesamount
    model=3
    minesamount=99
    x=0
    y=2
    modelx=30
    modely=16
    borderx=30
    bordery=24
    initialx=0
    initialy=2
    #把格子以50*50為一格畫線
    for i in range(int(modelx)):
        for j in range(int(modely)):
            cvs.create_rectangle(i*50,j*50+100,i*50+50,j*50+150,fill='white',outline='black')

    for i in range(int(modely)):
        loadmap.append([])
        minesmap.append([])
        bannersmap.append([])
        latticemap.append([])
        for j in range(int(modelx)):
            loadmap[i].append(0)
            minesmap[i].append('F')
            bannersmap[i].append(False)
            latticemap[i].append(False)




    #在地圖上隨機取地雷的座標
    while n<minesamount:
        a=[random.randint(0,int(modelx)-1),random.randint(0,int(modely)-1)]
        if a in minesxy:
            continue
        minesxy.append(a)
        n+=1
        print(minesxy)



    #將為地圖被標記的座標狀態改為True
    for i in range(len(minesxy)):
        minesmap[minesxy[i][1]][minesxy[i][0]]='T'
        #做出每個位置的附近的地雷數
        if minesxy[i][0]==0:                                            #第1種可能
            if minesxy[i][1]!=0 and minesxy[i][1]!=modely-1:                       #第1-1種可能
                for j in range(0,3):
                    for k in range(1,3):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
            elif minesxy[i][1]==0:                                      #第1-2種可能
                for j in range(1,3):
                    for k in range(1,3):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
            elif minesxy[i][1]==modely-1:                                      #第1-3種可能
                for j in range(0,2):
                    for k in range(1,3):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
        elif minesxy[i][0]==modelx-1:                                          #第2種可能
            if minesxy[i][1]!=0 and minesxy[i][1]!=modely-1:                       #第2-1種可能
                for j in range(0,3):
                    for k in range(0,2):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
            elif minesxy[i][1]==0:                                      #第2-2種可能
                for j in range(1,3):
                    for k in range(0,2):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
            elif minesxy[i][1]==modely-1:                                      #第2-3種可能
                for j in range(0,2):
                    for k in range(0,2):
                        loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
        elif minesxy[i][1]==0:                                          #第3種可能
            for j in range(1,3):
                for k in range(0,3):
                    loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
        elif minesxy[i][1]==modely-1:                                          #第4種可能
            for j in range(0,2):
                for k in range(0,3):
                    loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1
        else:                                                       #第5種可能
            for j in range(0,3):
                for k in range(0,3):
                    loadmap[minesxy[i][1]-1+j][minesxy[i][0]-1+k]+=1

    #檢查附近地雷數量
    #for i in range(10):
    #   print(loadmap[i])
    #檢查地雷分佈位置
    #for i in range(10):
    #   print(minesmap[i])

    #將格子附近的地雷數標記出來
    for i in range(int(modely)):
        for j in range(int(modelx)):
            if loadmap[i][j]!=0:
                mynumbers=cvs.create_text(j*50+25,i*50+125,text=loadmap[i][j],anchor='center')

    #將地雷的圖片放上
    for i in range(minesamount):
        cvs.create_image(minesxy[i][0]*50,minesxy[i][1]*50+100,image=mines,anchor='nw',tag='tag_mines')

    #將格子放上畫布
    for i in range(int(modely)):
        for j in range(int(modelx)):
            cvs.create_image(j*50,i*50+100,image=lattice,anchor='nw',tag='tag_lattice'+str(j)+','+str(i))
                
    #將玩家放上畫布
    cvs.create_image(x*50,y*50,image=figure,anchor='nw',tag='tag_figure')

    #刪除個難度的檢視圖
    cvs.delete('tag_simple')
    cvs.delete('tag_common')
    cvs.delete('tag_difficult')

    #刪除選擇模式按鈕
    btn1.destroy()
    btn2.destroy()
    btn3.destroy()

    lab1.destroy() 

    #開始按鈕
    btn=tk.Button(cvs,text='遊戲開始',command=startgame,)
    btn.place(x=730,y=40)

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
    countdown()

#計時開始
def countdown():
    global count,labtime
    if counts==True:
        exit()
    labtime=tk.Label(form,text='遊戲時長:'+str(count)+'秒',font=('微軟正黑體',17,'bold'),fg='red')
    labtime.place(x=1000,y=50)
    count+=1
    labtime.after(1000,countdown)

#紀錄遊戲成績
def scoring():
    f=open('score.dat','a')#開啟一個可以寫入的資料檔，檔名是score.dat
    f.writelines(name.get()+str(labtime['text'])+'\n')
    f.close

#設定的介面
def settings():
    global name
    lab0.destroy()
    textbox.destroy()
    btn.destroy()
    list1.destroy()

    lab1.place(x=680,y=700)

    cvs.create_image(150,280,image=simple,anchor='nw',tag='tag_simple')#初級的檢視圖
    cvs.create_image(610,250,image=common,anchor='nw',tag='tag_common')#中級的檢視圖
    cvs.create_image(990,250,image=difficult,anchor='nw',tag='tag_difficult')#高級的檢視圖

    btn1.place(x=210,y=580)
    btn2.place(x=710,y=580)
    btn3.place(x=1210,y=580)

#設計一個排名介面
def rank():
    #for i in range(len(textbox)):
    #    textbox.delete(0,'end')
    f=open('.\score.dat','r')#打開score.dat這個檔案
    rec=f.readline()#讀取一筆資料並存在rec變數內
    while rec!='':
        list1.insert(tk.END,rec)#並將目前的這一個分數(插入)到清單內
        rec=f.readline()#讀取下一筆分數
    f.close
    

    lab0.place(x=580,y=385)
    textbox.place(x=700,y=395)
    btn.place(x=670,y=500)
    list1.place(x=850,y=300)

#一開始的主視窗
form=tk.Tk()
form.geometry('1500x900')
form.title('踩地雷')

#放上畫布
cvs=tk.Canvas(width='1500',height='900',bg='lightgreen')
cvs.pack()

#紀錄的功能表
cvs.create_rectangle(0,0,1500,100,fill='grey')

#叫出圖片
figure=tk.PhotoImage(file='./images/figure.png')#玩家(主角)
mines=tk.PhotoImage(file='./images/mines.png')#地雷
lattice=tk.PhotoImage(file='./images/lattice.png')#格子
banner=tk.PhotoImage(file='./images/banner.png')#旗幟
simple=tk.PhotoImage(file='./images/simple.png')#初級的圖片
common=tk.PhotoImage(file='./images/common.png')#中級的圖片
difficult=tk.PhotoImage(file='./images/difficult.png')#高級的圖片

btn=tk.Button(text='確認名字',font=('微軟正黑體',15,'bold'),fg='blue',command=settings)#確認玩家名字的按鈕
btn1=tk.Button(cvs,text='初級',width='10',fg='green',command=simplebg)#初級的按鈕
btn2=tk.Button(cvs,text='中級',width='10',fg='yellow',command=commonbg)#中級的按鈕
btn3=tk.Button(cvs,text='高級',width='10',fg='red',command=difficultbg)#高級的按鈕

lab0=tk.Label(text='玩家姓名:',font=('微軟正黑體',19,'bold'),fg='brown',bg='lightgreen')
lab1=tk.Label(text='請選擇難度!',font=('微軟正黑體',19,'bold'),fg='brown',bg='lightgreen')

name=tk.StringVar()
textbox=tk.Entry(textvariable=name,width=20,)#產生一個可以輸入文字的(文字盒)

list1=tk.Listbox(width=20,font=('微軟正黑體',14,'bold'),fg='blue')

#叫出音效
pygame.mixer.init()#將音效初始化
pop=pygame.mixer.Sound('./music/pop.wav')

rank()


form.mainloop()