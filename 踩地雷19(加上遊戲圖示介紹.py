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
walks=[]
walkabove=0#紀錄向上走的狀態
walkunder=0#紀錄向下走的狀態
walkleft=0#紀錄向左走的狀態
walkright=0#紀錄向右走的狀態
minesamount=0#個難度地圖的地雷數
a=0#一開始隨機取的炸彈x座標
b=0#一開始隨機取的炸彈y座標
minesxy=[]#記錄所有取的炸彈x,y座標
n=0#隨機取c個炸彈
c=0#紀錄標記起來的地雷數
loadmap=[]#每個格子附近的地雷數
minesmap=[]#地雷地圖位置
bannersmap=[]#插旗地圖位置
banneramount=0#最多能放的旗幟數
latticemap=[]#格子地圖位置
et=[]#Expandterritory
preet=[]#用來儲存已Expandterritory的座標
etmines=0#用來記錄當前位置附近的炸彈數

#角色的操控
def key_down(e):
    global key
    key=e.keysym
    print(key)#檢查點

def key_up(e):
    global key
    key=''

def player_walk():
    global x,y,et,c,counts,c1,c2,walkabove,walkunder,walkleft,walkright,banneramount
    if key=='w':#向上走
        y-=1
        cvs.delete('tag_figure')
        if y<initialy:#此將偵測邊界的程式移到交換走路圖片之前
            y=initialy
        if walkabove==0:
            c1='tag_above2'
            c2='above02'
            above02=cvs.create_image(x*50,y*50,image=above2,anchor='nw',tag='tag_above2')
            walks.append(above02)
            form.after(100,delete_walk,above02)
            walkabove+=1
        elif walkabove==1:
            c1='tag_above4'
            c2='above04'
            above04=cvs.create_image(x*50,y*50,image=above4,anchor='nw',tag='tag_above4')
            walks.append(above04)
            form.after(100,delete_walk,above04)
            walkabove-=1
    if key=='s':#向下走
        y+=1
        cvs.delete('tag_figure')
        if y>initialy+modely-1:
            y=initialy+modely-1
        if walkunder==0:
            c1='tag_under2'
            c2='under02'
            under02=cvs.create_image(x*50,y*50,image=under2,anchor='nw',tag='tag_under2')
            walks.append(under02)
            form.after(100,delete_walk,under02)
            walkunder+=1
        elif walkunder==1:
            c1='tag_under4'
            c2='under04'
            under04=cvs.create_image(x*50,y*50,image=under4,anchor='nw',tag='tag_under4')
            walks.append(under04)
            form.after(100,delete_walk,under04)
            walkunder-=1
    if key=='a':#向左走
        x-=1
        cvs.delete('tag_figure')
        if x<initialx:
            x=initialx
        if walkleft==0:
            c1='tag_left2'
            c2='left02'
            left02=cvs.create_image(x*50,y*50,image=left2,anchor='nw',tag='tag_left2')
            walks.append(left02)
            form.after(100,delete_walk,left02)
            walkleft+=1
        elif walkleft==1:
            c1='tag_left4'
            c2='left04'
            left04=cvs.create_image(x*50,y*50,image=left4,anchor='nw',tag='tag_left4')
            walks.append(left04)
            form.after(100,delete_walk,left04)
            walkleft-=1
    if key=='d':#向右走
        x+=1
        cvs.delete('tag_figure')
        if x>initialx+modelx-1:
            x=initialx+modelx-1
        if walkright==0:
            c1='tag_right2'
            c2='right02'
            right02=cvs.create_image(x*50,y*50,image=right2,anchor='nw',tag='tag_right2')
            walks.append(right02)
            form.after(100,delete_walk,right02)
            walkright+=1
        elif walkright==1:
            c1='tag_right4'
            c2='right04'
            right04=cvs.create_image(x*50,y*50,image=right4,anchor='nw',tag='tag_right4')
            walks.append(right04)
            form.after(100,delete_walk,right04)
            walkright-=1
    if key=='e':#挖開格子
        if minesmap[y-initialy][x-initialx]=='F':
            cvs.delete('tag_lattice'+str(x-initialx)+','+str(y-initialy))
            #preet.append([x-initialx,y-initialy])
            latticemap[y-initialy][x-initialx]=True
            ###判斷玩家所在位置挖開的附近是否有空地
            if loadmap[y-initialy][x-initialx]==0:
                et.append([x-initialx,y-initialy])
                #print(et)#檢查點
                Expandterritory0()#如果人物底下是0則執行展地
            if loadmap[y-initialy][x-initialx]!=0:
                et.append([x-initialx,y-initialy])
                #print(et)#檢查點
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
                if banneramount>0:
                    cvs.create_image(x*50,y*50,image=banner,anchor='nw',tag='tag_banner'+str(x-initialx)+str(y-initialy))
                    minesmap[y-initialy][x-initialx]=minesmap[y-initialy][x-initialx]+'banner'
                    banneramount-=1
                    banneramount0()
            else:
                cvs.delete('tag_banner'+str(x-initialx)+str(y-initialy))
                minesmap[y-initialy][x-initialx]=list(minesmap[y-initialy][x-initialx])[0]
                banneramount+=1
                banneramount0()
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

#刪除上一個動作的圖片
def delete_walk(c2):
    cvs.delete(c1)
    cvs.create_image(x*50,y*50,image=figure,anchor='nw',tag='tag_figure')
    cvs.coords('tag_figure',x*50,y*50)
    walks.remove(c2)

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
            #print(et)#檢查點
            #print(preet)#檢查點
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
                    #print(et)#檢查點
    else:
        for i in range(len(et)): 
            et.pop(0)
    etmines
    
#一開始的遊戲難度設定
#簡單模式
def simplebg():   
    global mynumbers,n,x,y,modelx,modely,model,borderx,bordery,initialx,initialy,minesamount,banneramount
    model=1
    minesamount=10
    banneramount=10
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
    
    #生成地圖所需的二維串列
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
        #print(minesxy)#檢查點

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
    global mynumbers,n,x,y,modelx,modely,model,borderx,bordery,initialx,initialy,minesamount,banneramount
    model=2
    minesamount=40
    banneramount=40
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

    #生成地圖所需的二維串列
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
        #print(minesxy)#檢查點

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
    global mynumbers,n,x,y,modelx,modely,model,borderx,bordery,initialx,initialy,minesamount,banneramount
    model=3
    minesamount=99
    banneramount=99
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

    #生成地圖所需的二維串列
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
        #print(minesxy)#檢查點

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

#開始遊戲
def startgame():
    player_walk()
    countdown()
    banneramount0()

#計時開始
def countdown():
    global count,labtime,banneramount
    if counts==True:
        exit()
    labtime=tk.Label(form,text='遊戲時長:'+str(count)+'秒',font=('微軟正黑體',17,'bold'),fg='red')
    labtime.place(x=1000,y=50)#放上計時器
    count+=1
    labtime.after(1000,countdown)

#放上旗幟總數
def banneramount0():
    labbanneramount=tk.Label(form,text=banneramount,width=10,font=('微軟正黑體',17,'bold'),fg='red')
    labbanneramount.place(x=400,y=50)
    
#紀錄遊戲成績
def scoring():
    f=open('score.dat','a')#開啟一個可以寫入的資料檔，檔名是score.dat，'a'是寫入append
    f.writelines(tag_textbox.get()+','+str(labtime['text'])+','+str(model)+'\n')
    f.close

#設定的介面
def settings():
    global tag_textbox
    lab0.destroy()
    textbox.destroy()
    btn.destroy()
    list1.destroy()
    list2.destroy()
    mylabel0.destroy()
    mylabel1.destroy()
    mylabel2.destroy()
    mylabel3.destroy()
    mylabel4.destroy()
    mylabel5.destroy()
    mylabel6.destroy()
    mylabel7.destroy()
    mylabel8.destroy()
    mylabel9.destroy()
    mylabel10.destroy()
    mylabel11.destroy()
    mylabel12.destroy()
    mylabel13.destroy()
    btnrank1.destroy()
    btnrank2.destroy()
    btnrank3.destroy()
    cvs.delete('tag_rectangle')
    cvs.delete('tag_keyboard')
    cvs.delete('tag_mines')
    cvs.delete('tag_banner')

    lab1.place(x=680,y=700)

    cvs.create_image(150,280,image=simple,anchor='nw',tag='tag_simple')#初級的檢視圖
    cvs.create_image(610,250,image=common,anchor='nw',tag='tag_common')#中級的檢視圖
    cvs.create_image(990,250,image=difficult,anchor='nw',tag='tag_difficult')#高級的檢視圖

    btn1.place(x=210,y=580)
    btn2.place(x=710,y=580)
    btn3.place(x=1210,y=580)

#設計一個排名介面
#一開始的排名
def rank():
    f=open('.\score.dat','r')#打開score.dat這個檔案，'r'是讀取read
    rec=(f.readline()).split(',')#讀取下一筆分數
    while rec!=['']:
        #print(rec)#檢查點
        rec0=rec[0]
        rec1=rec[1]#讀取一筆資料並存在rec變數內
        list1.insert(tk.END,rec0)#並將目前的這一個分數(插入)到清單內
        list2.insert(tk.END,rec1)
        rec=(f.readline()).split(',')#讀取一筆資料並存在rec變數內
        f.close#關閉score.dat這個檔案

    #繪製背景框
    cvs.create_rectangle(80,200,760,760,fill='#a0a0a0',tag='tag_rectangle')

    #遊戲說明
    mylabel0.place(x=100,y=220) 
    mylabel1.place(x=100,y=275) 
    mylabel2.place(x=100,y=305) 
    mylabel3.place(x=100,y=335) 
    mylabel4.place(x=100,y=365) 
    mylabel5.place(x=100,y=500) 
    mylabel6.place(x=100,y=555) 
    mylabel7.place(x=100,y=585) 
    mylabel8.place(x=100,y=615) 
    mylabel9.place(x=100,y=645) 
    mylabel10.place(x=100,y=675) 
    mylabel11.place(x=100,y=705) 
    #鍵盤示意圖
    cvs.create_image(500,530,image=keyboard,anchor='nw',tag='tag_keyboard')
    #遊戲圖示介紹
    cvs.create_image(325,600,image=mines,anchor='nw',tag='tag_mines')
    mylabel12.place(x=370,y=620)
    cvs.create_image(330,680,image=banner,anchor='nw',tag='tag_banner')
    mylabel13.place(x=370,y=690)

    lab0.place(x=800,y=385)
    textbox.place(x=920,y=395)
    btn.place(x=890,y=500)
    btnrank1.place(x=1150,y=240)
    btnrank2.place(x=1245,y=240)
    btnrank3.place(x=1340,y=240)
    list1.place(x=1150,y=270)
    list2.place(x=1263,y=270)
#初級的排名
def rank1():
    f=open('.\score.dat','r')#打開score.dat這個檔案，'r'是讀取read
    list1.delete(0,'end')#清除原先的名字欄
    list2.delete(0,'end')#清除原先的成績欄
    rec=(f.readline()).split(',')#讀取下一筆分數
    while rec!=['']:
        print(rec)
        if int(rec[2])==1:
            rec0=rec[0]
            rec1=rec[1]#讀取一筆資料並存在rec變數內
            list1.insert(tk.END,rec0)#並將目前的這一個分數(插入)到清單內
            list2.insert(tk.END,rec1)
        rec=(f.readline()).split(',')#讀取一筆資料並存在rec變數內
    f.close#關閉score.dat這個檔案
#中級的排名
def rank2():
    f=open('.\score.dat','r')#打開score.dat這個檔案，'r'是讀取read
    list1.delete(0,'end')#清除原先的名字欄
    list2.delete(0,'end')#清除原先的成績欄
    rec=(f.readline()).split(',')#讀取下一筆分數
    while rec!=['']:
        print(rec)
        if int(rec[2])==2:
            rec0=rec[0]
            rec1=rec[1]#讀取一筆資料並存在rec變數內
            list1.insert(tk.END,rec0)#並將目前的這一個分數(插入)到清單內
            list2.insert(tk.END,rec1)
        rec=(f.readline()).split(',')#讀取一筆資料並存在rec變數內
    f.close#關閉score.dat這個檔案
#高級的排名
def rank3():
    f=open('.\score.dat','r')#打開score.dat這個檔案，'r'是讀取read
    list1.delete(0,'end')#清除原先的名字欄
    list2.delete(0,'end')#清除原先的成績欄    
    rec=(f.readline()).split(',')#讀取下一筆分數
    while rec!=['']:
        print(rec)
        if int(rec[2])==3:
            rec0=rec[0]
            rec1=rec[1]#讀取一筆資料並存在rec變數內
            list1.insert(tk.END,rec0)#並將目前的這一個分數(插入)到清單內
            list2.insert(tk.END,rec1)
        rec=(f.readline()).split(',')#讀取一筆資料並存在rec變數內
    f.close#關閉score.dat這個檔案

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
keyboard=tk.PhotoImage(file='./images/keyboard.png')#高級的圖片

#叫出圖片(移動動作)
above1=tk.PhotoImage(file='./images/動作/above1.png')#玩家向上走動作1
above2=tk.PhotoImage(file='./images/動作/above2.png')#玩家向上走動作2
above3=tk.PhotoImage(file='./images/動作/above3.png')#玩家向上走動作3
above4=tk.PhotoImage(file='./images/動作/above4.png')#玩家向上走動作4
under1=tk.PhotoImage(file='./images/動作/under1.png')#玩家向下走動作1
under2=tk.PhotoImage(file='./images/動作/under2.png')#玩家向下走動作2
under3=tk.PhotoImage(file='./images/動作/under3.png')#玩家向下走動作3
under4=tk.PhotoImage(file='./images/動作/under4.png')#玩家向下走動作4
left1=tk.PhotoImage(file='./images/動作/left1.png')#玩家向左走動作1
left2=tk.PhotoImage(file='./images/動作/left2.png')#玩家向左走動作2
left3=tk.PhotoImage(file='./images/動作/left3.png')#玩家向左走動作3
left4=tk.PhotoImage(file='./images/動作/left4.png')#玩家向左走動作4
right1=tk.PhotoImage(file='./images/動作/right1.png')#玩家向右走動作1
right2=tk.PhotoImage(file='./images/動作/right2.png')#玩家向右走動作2
right3=tk.PhotoImage(file='./images/動作/right3.png')#玩家向右走動作3
right4=tk.PhotoImage(file='./images/動作/right4.png')#玩家向右走動作4

#設置按鈕區
btn=tk.Button(text='確認名字',font=('微軟正黑體',15,'bold'),fg='blue',command=settings)#確認玩家名字的按鈕
btn1=tk.Button(cvs,text='初級',width='10',fg='green',command=simplebg)#初級的按鈕
btn2=tk.Button(cvs,text='中級',width='10',fg='yellow',command=commonbg)#中級的按鈕
btn3=tk.Button(cvs,text='高級',width='10',fg='red',command=difficultbg)#高級的按鈕
btnrank1=tk.Button(cvs,text='初級',width='12',command=rank1)#初級的按鈕
btnrank2=tk.Button(cvs,text='中級',width='12',command=rank2)#中級的按鈕
btnrank3=tk.Button(cvs,text='高級',width='12',command=rank3)#高級的按鈕

#設置標籤
lab0=tk.Label(text='玩家姓名:',font=('微軟正黑體',19,'bold'),fg='brown',bg='lightgreen')
lab1=tk.Label(text='請選擇難度!',font=('微軟正黑體',19,'bold'),fg='brown',bg='lightgreen')

#設置文字盒
tag_textbox=tk.StringVar()
textbox=tk.Entry(textvariable=tag_textbox,width=20)#產生一個可以輸入文字的(文字盒)

#紀錄文字盒輸入的資料(列表選擇框)
list1=tk.Listbox(width=10,height=20,font=('微軟正黑體',14,'bold'),fg='blue')
list2=tk.Listbox(width=15,height=20,font=('微軟正黑體',14,'bold'),fg='blue')

#遊戲說明
mylabel0=tk.Label(form, text='踩地雷規則:',font=('微軟正黑體',30,'bold'),bg='#a0a0a0')
mylabel1=tk.Label(form, text='踩地雷難度分為初級、中級、高級，初級的格子數為9*9、地雷數為10顆',font=('微軟正黑體',15,'bold'),bg='#a0a0a0')
mylabel2=tk.Label(form, text='中級的格子數為16*16、地雷數為40顆，高級的格子數為30*16、地雷數',font=('微軟正黑體',15,'bold'),bg='#a0a0a0')
mylabel3=tk.Label(form, text='為99顆，要將所有地雷用旗幟標誌出來即可完成遊戲，挖到地雷時則失敗',font=('微軟正黑體',15,'bold'),bg='#a0a0a0')
mylabel4=tk.Label(form, text='並結束遊戲。',font=('微軟正黑體',15,'bold'),bg='#a0a0a0')
mylabel5=tk.Label(form, text='遊戲按鍵:',font=('微軟正黑體',30,'bold'),bg='#a0a0a0')
mylabel6=tk.Label(form, text='按鍵盤W向上走',font=('微軟正黑體',15,'bold'),bg='#a0a0a0')
mylabel7=tk.Label(form, text='按鍵盤A向左走',font=('微軟正黑體',15,'bold'),bg='#a0a0a0')
mylabel8=tk.Label(form, text='按鍵盤S向左走',font=('微軟正黑體',15,'bold'),bg='#a0a0a0')
mylabel9=tk.Label(form, text='按鍵盤D向左走',font=('微軟正黑體',15,'bold'),bg='#a0a0a0')
mylabel10=tk.Label(form, text='按鍵盤E挖開格子',font=('微軟正黑體',15,'bold'),bg='#a0a0a0')
mylabel11=tk.Label(form, text='按鍵盤Q插上旗幟',font=('微軟正黑體',15,'bold'),bg='#a0a0a0')
mylabel12=tk.Label(form, text='：地雷',font=('微軟正黑體',15,'bold'),bg='#a0a0a0')
mylabel13=tk.Label(form, text='：旗幟',font=('微軟正黑體',15,'bold'),bg='#a0a0a0')

#叫出音效
pygame.mixer.init()#將音效初始化
pop=pygame.mixer.Sound('./music/pop.wav')

#排名函式(在遊戲結束時執行，將此次遊玩時長紀錄)
rank()

form.mainloop()