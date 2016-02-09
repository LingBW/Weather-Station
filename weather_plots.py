# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 14:20:18 2016

@author: bling
"""

# plot circles (like I did in high school)
     
import math, sys, random
from Tkinter import *
from tkMessageBox import *
import serial
import numpy as np
import datetime
import time

     
ser = serial.Serial('/dev/ttyUSB0',9600,timeout=30)
#ser = serial.Serial('COM16', 9600)                #   in Windows
#weather_data = []

def plotter():
    #angle = random.uniform(0,360)
    try:
        mes = ser.readline()
        mes = mes.split(',')
        mes = mes[:-1]
        #print mes
    
        mes[12]
    except:
        #print 'No data transmitted this moment.'
        canvas.delete('text')
        canvas.delete('lines')
        canvas.create_text(170,40,text='No Data Transmitted',tags='text',font=('times',20,'underline'))
        #pass
    else:
        
        angle = int(mes[4])
        AT = mes[6]
        WS = mes[3]
        DT = mes[1]+' '+mes[2]
        #print len(mes),type(mes)
        #weather_data.append(mes[:-1])
        
        x0, y0 = (200,200)
        
        radian = angle*(math.pi / 180)
        radius = 110 # 20+10*float(WS)
        
        #U = (float(WS)*0.5144444)*math.sin(radian)
        #V = (float(WS)*0.5144444)*math.cos(radian)
        #print 'U,V', U,V
        x1 = x0 + int( round( radius * math.sin(radian) )) 
        y1 = y0 - int( round( radius * math.cos(radian) ))
        #x1 = x0 - int( round( radius * math.sin(radian) )) 
        #y1 = y0 + int( round( radius * math.cos(radian) ))
        #x2 = x0 + int( round( radius * math.sin(radian) )) 
        #y2 = y0 - int( round( radius * math.cos(radian) ))
        if float(WS) >= 64.:
            clr = colors[12]
        else:
            for i in range(13):
                if float(WS) <= cat[i]:
                    clr = colors[i]
                    break
        Faht = 9.0/5.0 * float(AT) + 32 # Convert Celsius to Fahrenheit
        
        canvas.delete('text')
        canvas.delete('lines')
        
        #times = datetime.datetime.now()
        times = datetime.datetime.strptime(DT,"%y/%m/%d %H:%M:%S")
        times = times.strftime('%b %d, %H:%M')
        #canvas.delete('times')
        
        canvas.create_text(300,380,text=times,tags='text',font=('impact',16,'normal'))
        #canvas.coords("line", x1,y1,x2,y2)
        
        canvas.create_text(100,100,text=WS,tags='text',font=('times',20,'underline'),fill='blue')
        canvas.create_text(320,20,text='%.1f'%Faht,tags='text',font=('times',20,'underline'),fill='red')
        canvas.create_line(x0,y0,x1,y1, tag='lines',arrow=LAST,arrowshape=(18,20,18),width=10,fill=clr)#,dash=(7,4*int(radian)+1)
        #wt = Label(canvas,text='%d'%angle)
        #wt.pack()
        #canvas.create_window(100,100,window=wt)
    canvas.after(30000,plotter)
     
def makewindcanvas(root):
    canvas.create_oval(90,90,310,310,fill='blue',width=0)
    canvas.create_line(80,200,330,200, tag='xline',arrow=LAST,arrowshape=(8,10,8),width=2,fill='gray',dash=(5,4))
    canvas.create_text(335,215,text='E',font=('times',20,'italic'))
    canvas.create_line(200,320,200,70, tag='yline',arrow=LAST,arrowshape=(8,10,8),width=2,fill='gray',dash=(5,4))
    canvas.create_text(220,80,text='N',font=('times',20,'italic'),tag='north')
    canvas.create_text(100,78,text='KTS',font=('times',14,'italic'),tag='speed') #M/H,fill='gray'
    canvas.create_text(360,20,text=u"\xb0"+'F',font=('arial',20,'bold'),tag='tempurature') #u"\xb0"+'F'
    sx = 120; sy = 340; sy2 = sy+12
    for i in range(len(colors)):
        sx1 = sx+12*(i)
        canvas.create_rectangle(sx1,sy,sx1+12,sy2,fill=colors[i],width=0,tag='scale')
        
    #canvas.create_line(200,100, 200,300, tags=("line",), arrow="last",arrowshape=(18,20,18),width=10,fill='red',dash=(7,12))
    plotter()

def makemenu(root):
    menubar = Frame(root,bg='olive',bd=8)
    menubar.pack(side=TOP,fill=X,padx=4,pady=4)
    Button(menubar,text='file',command=sys.exit,font=('times',20,'bold'),fg='yellow',relief=RAISED,cursor='gumby',bd=4,bg='orange').pack(side=LEFT,fill=Y)
    Button(menubar,text='plot',command=(lambda:plot()),font=('times',20,'bold'),fg='yellow',relief=RAISED,cursor='gumby',bd=4,bg='orange').pack(side=LEFT,fill=Y)
    
def plot():
    canvas.delete(ALL)
    canvas.create_text(220,80,text='N',font=('times',20,'italic'))
    canvas.create_text(100,78,text='M/H',font=('times',20,'italic'))#'''
if __name__ == '__main__':
    root = Tk()
    root.title('Weather Station')
    root.protocol('WM_DELETE_WINDOW',lambda : showwarning('Weather Station Promgram', 'Sorry, Weather Station Window cannot be closed!'))#None
    #makemenu(root)
    #global canvas,colors#, scaleVar, checkVar 
    #colors = ['green','olive','yellow','orange','blue','magenta','red']#'cyan',
    cat = [1, 3, 6, 10, 16, 21, 27, 33, 40, 47, 55, 63, 64]
    colors = ['#FFFFFF','#CCFFFF','#99FFCC','#99FF99','#99FF66','#99FF00','#CCFF00','#FFFF00','#FFCC00','#FF9900','#FF6600','#FF3300','#FF0000']
    canvas = Canvas(root,width=400, height=400)#,bg='blue'
    canvas.pack(side=TOP)   
    makewindcanvas(root)                                     # on default Tk root
    mainloop()
