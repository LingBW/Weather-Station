# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 14:20:18 2016
Get data from weather station every minute.

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
#import win32gui,win32con,win32console
#from watchdog.observers import Observer
#from watchdog.events import LoggingEventHandler
  
print "Please do not close Weather-Station window."
#time.sleep(3)
# automactic minimize window
'''Minimize2 = win32gui.GetForegroundWindow()
time.sleep(1)
win32gui.ShowWindow(Minimize2,win32con.SW_MINIMIZE)
# disable close buttom of python window
hwnd = win32console.GetConsoleWindow()
if hwnd:
   hMenu = win32gui.GetSystemMenu(hwnd, 0)
   if hMenu:
       win32gui.DeleteMenu(hMenu, win32con.SC_CLOSE, win32con.MF_BYCOMMAND)#'''
       
# the deference between UTC and local time
utcti = datetime.datetime.utcnow(); utct = utcti.strftime('%H')
locti = datetime.datetime.now(); loct = locti.strftime('%H')
ditnu = int(utct)-int(loct)  
if ditnu < 0:
    ditnu = int(utct)+24-int(loct) #'''

     
#ser = serial.Serial('/dev/ttyUSB0',9600) #,timeout=30
#ser = serial.Serial('COM16', 9600)                #   in Windows
global weather_data, stime, transmit
weather_data = []
################ setting up ###################################################
stime = 120 #minutes, one hour is 60,send data interval
transmit = 'ON' # ON,OFF
save_raw_data = 'ON' # ON,OFF

def getdata():
    try:
        ser = serial.Serial('/dev/ttyUSB0',9600,timeout=30) #
        #ser = serial.Serial('COM26', 9600,timeout=30)                #   in Windows
    except :#OSError as en:
        #if en.errno == 2:
        print 'Weather Station USB-port connection problem!'
        raise Exception()
    
    try: 
        mes0 = ser.readline()
        #print 'Raw-data',mes0 # print raw data
        ser.close()
        
        mes = mes0.split(',')
        mes = mes[:-1]
        mes[12]
        if save_raw_data == 'ON':
            tf = open("weather-station1-output.dat", "a") # "a"-continue save data,"w"-start a new file when start running
            tf.write(mes0)
            tf.close()
    except:
        print 'No data transmitted from weather station. Check out the power supply of weather station'
        raise Exception()
    return mes
    
def transdata(wdata):
    mesnp = np.array(wdata)
    mesnpt = mesnp.T
    #time.sleep(40)
    AT = np.mean([float(i) for i in mesnpt[6]])+30 #'+30' means avoid negative value, Unit: celsius-Degree
    BP = np.mean([float(i) for i in mesnpt[8]]) # BAROMETER PRESSURE ( mb )
    RH = np.mean([float(i) for i in mesnpt[7]]) # RELATIVE HUMIDITY ( % )
    #VT = np.mean([float(i) for i in mesnpt[12]])
    ws = [float(i) for i in mesnpt[3]]
    wd = [float(i) for i in mesnpt[4]]
    
    #WD = np.mean([float(i) for i in mesnpt[4]])  # we can not average direction in this way
    WSU,WSV = [],[]
    for i in range(len(ws)):
        U = (ws[i]*0.5144444)*math.sin(wd[i]*math.pi/180)
        V = (ws[i]*0.5144444)*math.cos(wd[i]*math.pi/180)
        WSU.append(U); WSV.append(V)
    WU = np.mean(WSU); WV = np.mean(WSV) # meter per second#'''
    rad0 = math.atan2(WU,WV)
    WD = rad0*(180/math.pi) #wind direction, unit: degree   
    if WD<0:
        WD = WD+360
    WS = np.mean(ws)#*0.5144444 turn to m/s # wind speed,unit: kts
    #time.sleep(20)
    #print 'WU,WV,AT,BP,RH,VT',WU,WV,AT,BP,RH,VT,mesnpt[2][-1]
    #mes1 = '%.4d%.4d%.4d'%(WU*10,WV*10,AT*10)
    # Units: dedree,%,mb,kts,degree
    #mes1 = '%.3d%.3d%.5d%.3d%.4d'%(AT*10,RH*10,BP*10,WS*10,WD*10)
    mes1 = '%.3d%.3d%.4d%.3d%.3d'%(AT*10,RH*10,BP,WS*10,WD)
    #print 'WU,WV,AT 10-times',mes1
    #print 'AT3,RH3,BP5,WS3,WD4',mes1
    del weather_data[:] #empty the list

    # Send data to satellite
    
    try:
        try:
            ser1=serial.Serial('/dev/ttyUSB0',9600) # linux
            #ser1 = serial.Serial('COM27', 9600)              #   in Windows
        except OSError as en:
            if en.errno == 16 :
                time.sleep(180)
                ser1=serial.Serial('/dev/ttyUSB0',9600) # linux
                #ser1 = serial.Serial('COM27', 9600)              #   in Windows               
            else :              
                #print 'Transmitter USB-port connection problem!'
                raise
        time.sleep(1)
        ser1.writelines('\n')
        time.sleep(1)
        ser1.writelines('\n')
        time.sleep(1)
        ser1.writelines('yab'+'\n') # Force the given message to idle.
        time.sleep(5)
        ser1.writelines('\n')
        time.sleep(1)
        ser1.writelines('\n')
        time.sleep(1)
        #ser.writelines('ylb9'+meandepth+rangedepth+time_len+meantemp+sdeviatemp+'\n')
        ser1.writelines('ylb'+mes1+'\n')
        time.sleep(2) # 1100s 18 minutes
        ser1.close() # close port
        print 'Weather-station Sent Data: '+mes1
    except:
        print "Transmitter connection problem! Can't send data to satellite."
    
#################################################################################################################
def plotter():
    #angle = random.uniform(0,360)
    looptime = 59000
    try:
        #mes = ser.readline()
        mes = getdata()
        
    except:
        #print 'No data transmitted this moment.'
        canvas.delete('text')
        canvas.delete('lines')
        canvas.create_text(170,40,text='No Data Transmitted',tags='text',font=('times',20,'underline'))
        del weather_data[:] #empty the list if NO data transmitted
        #raise
    else:
        
        angle = int(mes[4])
        at = mes[6] #Unit: celsius-Degree
        bp = mes[8] # added by JiM 24 Apr 2016
        ws = mes[3] # unit: kts
        DT = mes[1]+' '+mes[2]
        ################################################Transmit#######################################
        weather_data.append(mes); #print len(weather_data),mes
        if len(weather_data)==stime:
            
            if transmit == 'ON':  
                try:
                    transdata(weather_data) #transmit data to AP3
                except:
                    print 'transdata function error!'
                looptime = looptime-13000
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
        if float(ws) >= 64.:
            clr = colors[12]
        else:
            for i in range(13):
                if float(ws) <= cat[i]:
                    clr = colors[i]
                    break
        Faht = 9.0/5.0 * float(at) + 32 # Convert Celsius to Fahrenheit
        
        canvas.delete('text')
        canvas.delete('lines')
        
        #times = datetime.datetime.now()
        times = datetime.datetime.strptime(DT,"%y/%m/%d %H:%M:%S")
        times = times - datetime.timedelta(hours=ditnu)
        times = times.strftime('%b %d, %H:%M')
        #canvas.delete('times')
        
        canvas.create_text(300,380,text=times,tags='text',font=('impact',16,'normal'))
        #canvas.coords("line", x1,y1,x2,y2)
        
        canvas.create_text(100,100,text=ws,tags='text',font=('times',20,'underline'),fill='blue')
        canvas.create_text(320,20,text='%.1f'%Faht,tags='text',font=('times',20,'underline'),fill='red')
        canvas.create_text(60,320,text=bp,tags='text',font=('times',20,'underline'),fill='black')
        canvas.create_line(x0,y0,x1,y1, tag='lines',arrow=LAST,arrowshape=(18,20,18),width=10,fill=clr)#,dash=(7,4*int(radian)+1)
        #wt = Label(canvas,text='%d'%angle)
        #wt.pack()
        #canvas.create_window(100,100,window=wt)
    canvas.after(looptime,plotter)
     
def makewindcanvas(root):
    canvas.create_oval(90,90,310,310,fill='blue',width=0)
    canvas.create_line(80,200,330,200, tag='xline',arrow=LAST,arrowshape=(8,10,8),width=2,fill='gray',dash=(5,4))
    canvas.create_text(335,215,text='E',font=('times',20,'italic'))
    canvas.create_line(200,320,200,70, tag='yline',arrow=LAST,arrowshape=(8,10,8),width=2,fill='gray',dash=(5,4))
    canvas.create_text(220,80,text='N',font=('times',20,'italic'),tag='north')
    canvas.create_text(100,78,text='KTS',font=('times',14,'italic'),tag='speed') #M/H,fill='gray'
    canvas.create_text(125,320,text='mb',font=('times',14,'italic'),tag='barop') #M/H,fill='gray'
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
    # Disable close buttom of TK
    root.protocol('WM_DELETE_WINDOW',lambda : showwarning('Weather Station Promgram', 'Sorry, Weather Station Window cannot be closed!'))#None
    #makemenu(root)
    #global canvas,colors#, scaleVar, checkVar 
    #colors = ['green','olive','yellow','orange','blue','magenta','red']#'cyan',
    cat = [1, 3, 6, 10, 16, 21, 27, 33, 40, 47, 55, 63, 64] # numbers stand for wind-speed(kts), aim for wind-range
    colors = ['#FFFFFF','#CCFFFF','#99FFCC','#99FF99','#99FF66','#99FF00','#CCFF00','#FFFF00','#FFCC00','#FF9900','#FF6600','#FF3300','#FF0000']
    canvas = Canvas(root,width=400, height=400)#,bg='blue'
    canvas.pack(side=TOP)   
    makewindcanvas(root)                                     # on default Tk root
    mainloop()
