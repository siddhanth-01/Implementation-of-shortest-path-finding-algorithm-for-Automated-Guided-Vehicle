# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 16:40:23 2021

@author: Sid
"""

# ------------------------- FINAL CODE ---------------------------------

import paho.mqtt.client as AgvClient
from PyQt5 import uic,QtWidgets
import sys

broker_ip = "broker.hivemq.com"
name = "Server_tx"
port = 1883
Publish_Topic = "path_tx"
Subscribe_Topic = "feedback"
Connected = False


def run():
    start = gui.start.text()
    end = gui.end.text()    

    try:      
        sx = int(start[0])
        ex = int(end[0])
        sy = int(start[1])
        ey = int(end[1])

        begin = [sx,sy]
        last = [ex,ey]
    
        
        p2 = []
        
        def y_change(sx,sy,ex,ey):
            if(sx == ex and sy >= ey):
                p2.append(begin)
                while(sy != ey):
                    sy = sy - 1
                    p2.append([sx,sy])
                if last not in p2:
                    p2.append(last)
                print("SX = EX AND SY > EY --> ", p2)

            elif(sx == ex and sy <= ey):
                p2.append(begin)
                while(sy != ey):
                    sy = sy + 1
                    p2.append([sx,sy])
                if last not in p2:
                    p2.append(last)
                print("SX = EX AND SY < EY --> ", p2)
                
            elif(sx >= ex and sy == ey):
                p2.append(begin)
                while(sx != ex):
                    sx = sx - 1
                    p2.append([sx,sy])
                if last not in p2:
                    p2.append(last)
                print("SX > EX AND SY = EY --> ", p2)

            elif(sx <= ex and sy == ey):
                p2.append(begin)
                while(sx != ex):
                    sx = sx + 1
                    p2.append([sx,sy])
                if last not in p2:
                    p2.append(last)
                print("SX < EX AND SY = EY --> ", p2)

            elif(sx<=ex and sy<=ey):              #This code is used when starting from low point to high point
                p2.append(begin)
                while(sx != ex and sy != ey):
                    sy = sy + 1
                    p2.append([int(start[0]),sy])
                    if(sy == ey):
                        while(sx != ex):
                            sx = sx + 1
                            p2.append([sx,sy])  
                        if last not in p2:
                            p2.append(last)
                    print("SX < EX AND SY < EY --> ", p2)
        
            elif(sx>=ex and sy<=ey):
                p2.append(begin)
                while(sx != ex and sy!= ey):
                    sy = sy + 1
                    p2.append([int(start[0]),sy])
                    if(sy == ey):
                        while(sx != ex):
                            sx = sx - 1
                            p2.append([sx,sy])
                        if last not in p2:
                            p2.append(last)
                    print("SX > EX AND SY < EY --> ", p2)
        
            #HIGH TO LOW [1,1] - [2,0]
            elif(sx<=ex and sy>=ey):
                p2.append(begin)
                while(sx != ex and sy!= ey):
                    sy = sy - 1
                    p2.append([int(start[0]),sy])
                    if(sy == ey):
                        while(sx != ex):
                            sx = sx + 1
                            p2.append([sx,sy])
                        if last not in p2:
                            p2.append(last)
                    print("SX < EX AND SY > EY --> ", p2)
                        
            else:                               #This code is used when starting from high point to low point
                p2.append(begin)
                while(sx != ex and sy != ey):
                    sy = sy - 1
                    p2.append([int(start[0]),sy])
                    if(sy == ey):
                        while(sx != ex):
                            sx = sx - 1
                            p2.append([sx,sy])  
                        if last not in p2:
                            p2.append(last)
                    print("Else --> ", p2)
        
        def convert_path(p):            #This code is used to convert nested list to string format
            temp = []
            for i in p:
                x = "".join(map(str,i))
                temp.append(x)
        
            temp = "".join(temp)
            return(temp)
        
        y_change(sx,sy,ex,ey)
        path1 = str("$") + convert_path(p2) + str("??%")
        #print(path1)
        #gui.message.append("Traversing through path: " + path1)
    
        
        def on_message(client, userdata, message):
            msg = str(message.payload)
            gui.message.append("X Coordinate: {}, Y Coordinate: {}, Orientation: {}".format(msg[2],msg[3],msg[4]))
        AGV.on_message= on_message                      #attach function to callback
            
        if(Connected == False):
            gui.message.append("No connection established")
        else:
            AGV.publish(Publish_Topic,path1)
            gui.message.append("Publishing path "+ path1)
            AGV.subscribe(Subscribe_Topic)
            gui.message.append("Subscribed...")
        
    except:
        gui.message.append("Please Enter Values ")
    
def connection():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            gui.message.append("Connected to broker")
            global Connected
            Connected = True
        else:
            gui.message.append("Connection failed",rc)

    AGV.connect(broker_ip,port)			            #connect to broker
    AGV.on_connect= on_connect                      #attach function to callback  
    AGV.loop_start()
    
def clear():
    AGV.loop_stop()
    AGV.disconnect()
    global Connected
    Connected = False
    gui.start.clear()
    gui.end.clear()
    gui.message.clear()
    gui.message.append("Disconnected")
    '''if(Connected == True):
        gui.message.clear()
        gui.message.append("Disconnected")
    else:
        gui.message.clear()
    '''
    
    
AGV = AgvClient.Client(name)	                #create a client name

application = QtWidgets.QApplication(sys.argv)

gui = uic.loadUi("app.ui")
gui.connect_btn.clicked.connect(connection)
gui.run_btn.clicked.connect(run)
gui.clear_btn.clicked.connect(clear)

gui.show()
sys.exit(application.exec())