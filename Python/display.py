################################################################
# TMS Integration -09-2017
################################################################

import serial
import binascii
import sys
import string
import bluetooth
from bluetooth import*
import bluetooth._bluetooth as _bt
import socket
import subprocess
import time

import struct

import glob
import logging
import logging.handlers

LOG_FILENAME = '/home/pi/Documents/TMS-Git/TMS-Python/log/loggingRotatingFileExample.log'

my_logger = logging.getLogger('myapp')
hdlr = logging.FileHandler(LOG_FILENAME)
formatter = logging.Formatter('%(asctime)s :%(levelname)s :%(message)s :')
hdlr.setFormatter(formatter)
my_logger.addHandler(hdlr) 
my_logger.setLevel(logging.DEBUG)




'''
def tcpSocketCreate(host, port, message)

    #create an INET, STREAMing socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print 'Failed to create socket'
        #sys.exit()

    print 'Socket Created'

    try:
        remote_ip = socket.gethostbyname( host )
        s.connect((host, port))

    except socket.gaierror:
        print 'Hostname could not be resolved. Exiting'
        #sys.exit()

    print 'Socket Connected to ' + host + ' on ip ' + remote_ip

    #Send some data to remote server
    #message = "Test"

    try :
        #Set the whole string
        while True:
            s.send(message)
            print 'Message sent successfully'
            time.sleep(1)
            print 'Sending...'
    except socket.error:
        #Send failed
        print 'Send failed'
        #sys.exit()


    
'
def recv_timeout(the_socket,timeout=2):
    #make socket non blocking
    the_socket.setblocking(0)

    #total data partwise in an array
    total_data=[];
    data='';

    #beginning time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break

        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break

        #recv something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass

    #join all parts to make final string
    return ''.join(total_data)

#get reply and print
print recv_timeout(s)

s.close()

'''
presint_Bar = 0
presint_Psi = 0
dispPsi = ""

pres = ""
temp = ""

tempint_Celcious = 0
disptemp = ""


Red = "1"
Green = "2"
Yellow ="3"
Blue = "4"
White = "7"
pres_color = ""
temp_color = ""

nC = ""

dispVar = ""
dispVar1 = ""
dispVar2 = ""
dispVar3 = ""
dispVar4 = ""
dispVar5 = ""
dispVar6 = ""


def displayPresValidation(pres):

    try:

        #Check for the Valid Pres is not 0000
        if pres.strip() != "0000" :
                        
            presint_Bar = ((int(pres, 16)*0.025))
            presint_Psi = int (round(presint_Bar * 14.5038))
            dispPsi = str((presint_Psi))
                        
                        
            #Staturated PSI value between 121 to 125 Should be Green Color
            if (presint_Psi) < 125 and presint_Psi >= 120:

                pres_color = Green
                #print pres_color
                        
            #Staturated PSI value between 121 to 125 Should be Yellow Color
            elif presint_Psi < 120 and presint_Psi >= 115:

                pres_color = Yellow

            #Staturated PSI value between 114 to below Should be Red Color
            elif presint_Psi < 114 :
                pres_color = Red

            #Staturated PSI value is above 125 Should be White Color
            elif presint_Psi > 125 :
                pres_color = White

            else:
                pres_color = Red
 
                        
        #Check for the Valid Pres is 0000
        else:
            pres_color = Blue
            dispPsi = "---"

        return  pres_color, dispPsi

    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Pressure Calculation:%s ",e)
        print ("Failed - Pressure Calculation: ",e)

        return None

def displayTempValidation(temp):

    try:
        #Check for the Valid Temp is not 00
        if  temp.strip() != "00":

            tempint_Celcious  = round(int(temp, 16) - 50)
            disptemp = str(int(tempint_Celcious))
                        
            #Staturated Temperature Celcious value between 50 to 45 Should be Yellow Color
            if tempint_Celcious < 50 and tempint_Celcious >= 45:
                temp_color = Green

            #Staturated Temperature Celcious value is above 50 Should be Red Color   
            elif tempint_Celcious >= 50:
                temp_color = Red

            #Staturated Temperature Celcious value is below 45 Should be Green Color
            elif tempint_Celcious < 45:
                temp_color = Green

            else:
                temp_color = Green
                            

        #Check for the Valid temp is 00
        else:
            temp_color = Blue
            disptemp = "---"

        return  temp_color, disptemp

    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Temperature Calculation:%s ",e)
        print ("Failed - Temperature Calculation: ",e)





def displayLEDBoard(vehName, dispCmd, date_time, dispVar):

    nC = White

    startChar = "["
    endChar   = "]"

    display =   "<\c"+nC+ "----" + ">" + "<\c"+ nC +"----------" + ">" + \
                "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
                "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
                "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" 

    vehName1  = "<\c"+nC+ "----" + ">"
    
    dispCmd1  = "<\c"+ nC +"----------" + ">"
    
    #dispVar1  = "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
    #            "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
    #            "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">"

    try:
        
        if (vehName != None) & (dispVar != None):

            vehN = vehName [4:8] #SND 9457
            print vehN

            vehNc = "<\c"+nC+ vehN + ">"

            dispc = dispCmd + " " + str(date_time)

            dispCmd1  = "<\c"+ nC + dispc + ">"

        display = startChar + vehNc + dispCmd1 + dispVar + endChar

        print display


    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - displayLEDBoard:%s ",e)
        print ("Failed - displayLEDBoard: ",e)


def displayLEDBoardParameters(mylist):

    

    nC = White

    dispVar =   "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
                "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
                "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" 


    dispVar1 = nC + " " + "---" + "\c" + nC + " " + "---"
    dispVar2 = nC + " " + "---" + "\c" + nC + " " + "---"
    dispVar3 = nC + " " + "---" + "\c" + nC + " " + "---"
    dispVar4 = nC + " " + "---" + "\c" + nC + " " + "---"
    dispVar5 = nC + " " + "---" + "\c" + nC + " " + "---"
    dispVar6 = nC + " " + "---" + "\c" + nC + " " + "---"

    try:

        if mylist !=  None:

            #print mylist
            #print len(mylist)
                    
            
            for i in range (2, len(mylist)):
                print i, mylist[i][6]
                
                if mylist[i][6] == '01' :

                    print "SensorID1 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]

                    pres_color, dispPsi = displayPresValidation(pres)
                    #print pres_color, dispPsi 
                    
                    temp_color, disptemp = displayTempValidation(temp)
                    #print temp_color, disptemp
                        
                    dispVar1 = pres_color +" "+ dispPsi + "\c" + temp_color + " " + disptemp

                    '''
                    dispVar = "<\c"+pres_color+" "+dispPsi+" \c"+temp_color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]

                    #if dispVar == "":
                        #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_color+" "+disptemp
                    #else:
                        #dispVar = dispVar + "/c3 "+mylist[i][10]+mylist[i][11]+ "/c4 "+mylist[i][12]+">"
                    '''

                elif mylist[i][6] == '02' :

                    print "SensorID2 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]
                    
                    pres_color, dispPsi = displayPresValidation(pres)
                    #print pres_color, dispPsi 
                    
                    temp_color, disptemp = displayTempValidation(temp)
                    #print temp_color, disptemp
                        
                    
                    #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_Color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]

                    dispVar2 = pres_color +" "+ dispPsi + "\c" + temp_color + " " + disptemp

                    '''
                    if dispVar == "":
                        nC = White
                        dispVar = "<\c"+nC+" "+"---" +"\c"+nC+" "+"---"+"\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp+">"
                    else:
                        dispVar = dispVar +" "+ "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp+">"
                    '''
                    
                elif mylist[i][6] == '03' :

                    print "SensorID3 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]
                    
                    pres_color, dispPsi = displayPresValidation(pres)
                    #print pres_color, dispPsi 
                    
                    temp_color, disptemp = displayTempValidation(temp)
                    #print temp_color, disptemp
                        
                    
                    #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_Color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]


                    dispVar3 =  pres_color +" "+ dispPsi + "\c" + temp_color + " " + disptemp
                    
                    '''
                    if dispVar == "":
                        nC = White
                        dispVar = "<\c"+nC+" "+"---" +"\c"+nC+" "+"---"+"\c"+nC+" "+nC+"\c"+nC+" "+nC+">"+"<\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp
                    else:
                        dispVar = dispVar +"<\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp
                    '''


                elif mylist[i][6] == '04' :

                    print "SensorID4 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]
                    
                    pres_color, dispPsi = displayPresValidation(pres)
                    #print pres_color, dispPsi 
                    
                    temp_color, disptemp = displayTempValidation(temp)
                    #print temp_color, disptemp
                        
                    
                    #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_Color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]

                    dispVar4 = pres_color +" "+ dispPsi + "\c" + temp_color + " " + disptemp

                    '''
                    if dispVar == "":
                        nC = White
                        dispVar = "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +       \
                                  "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp+">"
                    else:
                        dispVar = dispVar +" "+ "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp+">"
                    '''


                elif mylist[i][6] == '05' :

                    print "SensorID5 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]
                    
                    pres_color, dispPsi = displayPresValidation(pres)
                    #print pres_color, dispPsi 
                    
                    temp_color, disptemp = displayTempValidation(temp)
                    #print temp_color, disptemp
                        
                    
                    #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_Color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]

                    dispVar5 = pres_color +" "+ dispPsi + "\c" + temp_color + " " + disptemp

                    '''
                    if dispVar == "":
                        nC = White
                        dispVar = "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
                                  "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">"  +  \
                                  "<\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp
                    else:
                        dispVar = dispVar +" "+ "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp

                    '''

                    
                elif mylist[i][6] == '06' :

                    print "SensorID6 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]
                    
                    pres_color, dispPsi = displayPresValidation(pres)
                    #print pres_color, dispPsi 
                    
                    temp_color, disptemp = displayTempValidation(temp)
                    #print temp_color, disptemp
                        
                    
                    #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_Color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]

                    dispVar6 = pres_color +" "+ dispPsi + "\c" + temp_color + " " + disptemp

                    '''
                    if dispVar == "":
                        nC = White
                        dispVar = "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
                              "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">"  +  \
                              "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp +"\c"+pres_color+" "+dispPsi +"\c"+temp_color+" "+disptemp +">"
                    else:
                        dispVar = dispVar +" "+ "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp+">"+"]"

                    '''
      
                        #"<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
                        #"<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
                        #"<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" + "]"

                        #pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp

                        #" "+ "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp

            #dispVar1 = pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp
            #dispVar2 = pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp
                
            dispVar =   "<\c" + dispVar1 + "\c" + dispVar2 + ">"           \
                        "<\c" + dispVar3 + "\c" + dispVar4 + ">"           \
                        "<\c" + dispVar5 + "\c" + dispVar6 + ">"           
                        
            
            print dispVar

            return dispVar
        
    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Temperature Calculation:%s ",e)
        print ("Failed - Temperature Calculation: ",e)
        


'''
def displayLEDBoard(mylist):

    if mylist is not None:

        print mylist
        #print len(mylist), TPMSIdx
                
        dispVar = ""
        for i in range (len(mylist)):
            
            if mylist[i][6] == '01' :

                print "SensorID1 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                pres = mylist[i][10]+mylist[i][11]
                temp = mylist[i][12]

                l = int(pres, 16)*0.025
                k = str(int(l))
                
                #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                dispVar = "</c1 "+k+" /c2 "+mylist[i][12]
            
            if mylist[i][6] == '02' :

                print "SensorID 2",mylist[i][7]+mylist[i][8]+mylist[i][9]
                print "Pres",mylist[i][10]+mylist[i][11]
                print "Temp",mylist[i][12]
                if dispVar == "":
                    dispVar = "</c1 -- /c2 -- /c3 "+mylist[i][10]+mylist[i][11]+ "/c4 "+mylist[i][12]+">"
                else:
                    dispVar = dispVar + "/c3 "+mylist[i][10]+mylist[i][11]+ "/c4 "+mylist[i][12]+">"

            if mylist[i][6] == '03' :

                print "SensorID 3",mylist[i][7]+mylist[i][8]+mylist[i][9]
                print "Pres",mylist[i][10]+mylist[i][11]
                print "Temp",mylist[i][12]
                if dispVar == "":
                    dispVar = "</c1 -- /c2 -- /c3 -- /c4 -- ></c1 "+mylist[i][10]+mylist[i][11]+ "/c2 "+mylist[i][12]
                else:
                    dispVar = dispVar + "</c1 "+mylist[i][10]+mylist[i][11]+ "/c2 "+mylist[i][12]

            if mylist[i][6] == '04' :

                print "SensorID 4",mylist[i][7]+mylist[i][8]+mylist[i][9]
                print "Pres",mylist[i][10]+mylist[i][11]
                print "Temp",mylist[i][12]
                if dispVar == "":
                    dispVar = "</c1 -- /c2 -- /c3 -- /c4 -- ></c1 "+mylist[i][10]+mylist[i][11]+ "/c2 "+mylist[i][12]+">"
                else:
                    dispVar = dispVar + "</c1 "+mylist[i][10]+mylist[i][11]+ "/c2 "+mylist[i][12]+">"
    
        print dispVar
        

'''
#main function
if __name__ == "__main__":

    #if(len(sys.argv) < 2) :
        #print 'Usage : python client.py hostname'
        #sys.exit()

    #host = sys.argv[1]
    #port = 8888

    #message = "Test"

    dispCmd = "Sarojini Nagar Depot"

    vehName = "SND 9406"

    date_time = time.strftime('%H:%M:%S %d/%m/%Y')
    print date_time
    
    mylist = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
              [0, 'a1', '41', '08', '63', '00', '05'], \
              [0, 'a1', '41', '0f', '63', '00', '01', 'ba', '6b', '09', '01', '50', '78', '00'], \
              [0, 'a1', '41', '0f', '63', '00', '02', 'ba', '6d', '6d', '01', '25', '58', '00'], \
              [0, 'a1', '41', '0f', '63', '00', '03', '56', 'a8', 'cb', '01', '30', '70', '00'], \
              [0, 'a1', '41', '0f', '63', '00', '04', '56', 'a6', 'be', '01', '45', '65', '00'], \
              [0, 'a1', '41', '0f', '63', '00', '05', '56', 'a7', '81', '00', '00', '00', '00'], \
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


    displayLEDBoardParameters(mylist)

    dispVar = "<\c2 122\c1 70\c1 106\c2 38><\c1 110\c1 62\c3 118\c1 51><\c4 ---\c4 ---\c7 ---\c7 --->"

   

    displayLEDBoard(vehName, dispCmd, date_time, dispVar)

