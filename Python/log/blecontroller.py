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
global Tyre1No
global Tyre1ID
global Tyre1Presure
global Tyre1Temp

global Tyre2No
global Tyre2ID
global Tyre2Presure
global Tyre2Temp

global Tyre3No
global Tyre3ID
global Tyre3Presure
global Tyre3Temp
 
Tyre1No=""
Tyre1ID=""
Tyre1Presure=""
Tyre1Temp = ""
'''

Tyredata = []
T = []

# TPMS Bluetooth FMS request TPMS to send all recorded tyres data
def TpmsTireDataPosition():

    try:  
        #TpmsModuleQuery = ['\xAA', '\x41', '\xA1', '\x07', '\x63', '\x00']
        TpmsModuleQuery = ['AA', '41', 'A1', '07', '63', '00']
        #TpmsModuleQuery = ["AA", "41", "A1", "07", "63", "00"]

        #TpmsModuleQueryID = "AA41A1076300"
        if(TpmsModuleQuery != None):
            
            #print TpmsModuleQuery
            TpmsCksm = TpmsCalcChecksum(TpmsModuleQuery)
            
            TpmsModuleQueryID = ''.join(TpmsModuleQuery)
            #print TpmsModuleQuery
            
            #print TpmsCksm
            if(TpmsCksm != None):
                #Append checksum to the Query List
                TPMSQueryAllTyre = TpmsModuleQueryID + TpmsCksm
                TPMSQueryAllTyre = TPMSQueryAllTyre.strip()
                print TPMSQueryAllTyre
            else:
                my_logger.warning("Failed - Bluetooth Query checksum not Avalable: ",TpmsCksm)
                print("Failed - Bluetooth Query checksum not Avalable: ",TpmsCksm)
                return None

            my_hex_TPMS = TPMSQueryAllTyre.decode('hex')
            #print my_hex_TPMS       
            #print binascii.b2a_hex(my_hex_TPMS)

            #serial.write(my_hex_TPMS)

            return  my_hex_TPMS

        else:
            my_logger.warning("Failed - Bluetooth Query Command Value not Avalable: %s",TpmsModuleQuery)
            print("Failed - Bluetooth Query Command Value not Avalable: ",TpmsModuleQuery)
            return None

    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Bluetooth Query Command Value Error: %s, %s ",e, TpmsModuleQuery)
        print ("Failed - Bluetooth Query Command Value Error:",e, TpmsModuleQuery)

        return None


def Tpms_Tire_SET_Position1(L1, SID1):

    TpmsSET1 = ['AA', '41', 'A1', '0E', '63']

    try:  
    
        if(L1.strip(), SID1.strip() != None):
            TpmsSET1.append(L1)
            TpmsSET1.append(SID1[0:2])
            TpmsSET1.append(SID1[2:4])
            TpmsSET1.append(SID1[4:6])
                
            TpmsSET1.append('00')
            TpmsSET1.append('00')
            TpmsSET1.append('00')
            TpmsSET1.append('00')
        else:
            my_logger.warning("Failed - Bluetooth Query to SET Tyre Position1(Location, Sensor ID) not Avalable: %s, %s",L1, SID1)
            print ("Failed - Bluetooth Query to SET Tyre Position1(Location, Sensor ID) not Avalable: ",L1, SID1)
            return None

        if(TpmsSET1 != None):
            #print TpmsSET1
            TpmsCksm = TpmsCalcChecksum(TpmsSET1)
            #print TpmsCksm

            TpmsSET = ''.join(TpmsSET1)
            #print TpmsSET
            
            if(TpmsCksm != None):
                #Append checksum to the Query List
                TPMSQueryAddTyre = TpmsSET+(TpmsCksm)
                #print TPMSQueryAddTyre
            else:
                my_logger.warning("Failed - Bluetooth Query checksum not Avalable: ",TpmsCksm)
                print("Failed - Bluetooth Query checksum not Avalable: ",TpmsCksm)
                return None
            
            my_hex_TPMS = TPMSQueryAddTyre.decode('hex')
            #print my_hex_TPMS       
            print binascii.b2a_hex(my_hex_TPMS)

            return my_hex_TPMS
        
        else:
            my_logger.warning("Failed - Bluetooth Query to SET Tyre Position1(Location, Sensor ID) not Avalable: %s, %s, %s",L1, SID1, TpmsSET1)
            print ("Failed - Bluetooth Query to SET Tyre Position1(Location, Sensor ID) not Avalable: ",L1, SID1, TpmsSET1)
            return None
        
    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Bluetooth Query Attribute to Set (Location, Sensor ID) None: ",e, L1, SID1 )
        print ("Failed - Bluetooth Query Attribute to Set (Location, Sensor ID) None: ",e, L1, SID1 )

        return None


##################################################################################
#Need to Impliment the while loop for data send and receive as a sucessive method#   
##################################################################################
# TPMS Bluetooth to SET Tyre Data
def Tpms_SET_TireID(conn, TMSSET):

    try:
        
        if((TMSSET.strip() != None) & (conn != None)):
                
            #TPMSID1 = TpmsTireDataPosition()
            print binascii.b2a_hex(TMSSET)
            print "performing Bluetooth Communication..."

            while(True):
                try:
                    conn.send(TMSSET)
        
                    time.sleep(1)

                    data = conn.recv(1024)

                    hexstr = binascii.b2a_hex(data) 
                    RcvResponse =  hexstr[10:12]
                    #print RcvResponse
                    
                    if (RcvResponse == "aa"):
                        return hexstr
                    
                    else:
                        return None
                        break;
                
                except bluetooth.btcommon.BluetoothError as e:
                    my_logger.error("Failed - Bluetooth Socket data Send and Receive: %s", e)
                    print ("Failed - Bluetooth Socket data Send and Receive: ", e)  
                    conn.close()
                    time.sleep(2)
                    return None
                    pass

        else:
            my_logger.warning("Failed - Bluetooth Query to Send and Receive Command Not Available: %s",TMSSET)
            print("Failed - Bluetooth Query to Send and Receive Command Not Available: %s",TMSSET)
            return None

    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Bluetooth Query to Send and Receive Command Attribute Not Available: %s",e, TMSSET)
        print("Failed - Bluetooth Query to Send and Receive Command Attribute Not Available: %s",e, TMSSET)

        return None
                


#convert string to hex
def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)
    
    return reduce(lambda x,y:x+y, lst)

#convert hex repr to string
def toStr(s):
    return s and chr(int(s[:2], base=16)) + toStr(s[2:]) or ''

   

# TPMS Bluetooth Calculate Checksum
def TpmsCalcChecksum(TpmsModuleQuery1):

    try:
        count = len(TpmsModuleQuery1)
        #print TpmsModuleQuery1
        
        i = 0
        cksm = 0
        if(TpmsModuleQuery1 != None):
            
            while (i < count-1):
                #print(TpmsModuleQuery1[i])
                #val = binascii.b2a_hex(TpmsModuleQuery1[i])
                val = TpmsModuleQuery1[i].decode("hex")
                #cksm += int (val, 16)
                cksm += int(TpmsModuleQuery1[i], 16)
                #print cksm
                #i += 1
            
                cksm1 = hex(cksm).split('x')[-1]
                #cksm1 = hex(cksm)
                #print cksm1
                i += 1
            
            #print cksm1
            high, low = cksm1[:1], cksm1[1:3]
            #print(high, low)

            return low
        else:
            my_logger.warning("Failed - Bluetooth Query Command for Checksum is Not Available: %s", TpmsModuleQuery1)
            print ("Failed - Bluetooth Query Command for Checksum is Not Available: ", TpmsModuleQuery1)
            return None
    
    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Bluetooth Query Command for Checksum Query is Not Available:%s %s ",e, TpmsModuleQuery1)
        print ("Failed - Bluetooth Query Command for Checksum Query is Not Available: ", e,TpmsModuleQuery1)
        return None


'''
def TpmsCalcChecksum(TpmsModuleQuery1):

    count = len(TpmsModuleQuery1)
    #print TpmsModuleQuery1
    
    i = 0
    cksm = 0
    while (i < count-1):
        #print(TpmsModuleQuery1[i])
        val = binascii.b2a_hex(TpmsModuleQuery1[i])
        cksm += int (val, 16)

      
        cksm1 = hex(cksm).split('x')[-1]
        #cksm1 = hex(cksm)
        #print cksm1

        i += 1
        
    #print cksm1
    high, low = cksm1[:1], cksm1[1:3]
    #print(high, low)

    return low
'''
 
def connect_ble(BUID1):
    
    print "performing inquiry..."
    #serverMACAddress = '00:13:EF:C0:02:1E'
    port = 1
    
      
    '''
    nearby_devices = bluetooth.discover_devices(duration=4, lookup_names = True, flush_cache=True)

    print "found %d devices" % len(nearby_devices)

    for addr, name in nearby_devices:
        print "  %s - %s" % (addr, name)
    '''
    if(BUID1 != None):
        while(True):        
            print BUID1
            try:
                print "performing Bluetooth Socket Creation..."
                bleCon = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                #return bleCon
                break;

            except bluetooth.btcommon.BluetoothError as e:
                my_logger.error("Failed - Bluetooth Socket Creation: %s", e)
                print ("Failed - Bluetooth Socket Creation: ", e)
                #bleCon.close()
                time.sleep(2)
                #return None
                pass 

        print "trying to connect to %s on 0x%X" % (BUID1, port)

        if(bleCon is not None):
            while(True):
                try:
                    bleCon.connect((BUID1, port))
                        
                    print "connected to %s on 0x%X" % (BUID1, port)
                    print "performing Bluetooth Communication..."
                    return bleCon
                    break;

                except bluetooth.btcommon.BluetoothError as e:
                    print ("Failed Trying to connect on %s on 0x%X" % (BUID1, port),e)
                    my_logger.error("Failed - Trying to connect %s",e)  
                    time.sleep(2)
                    bleCon.close()
                    return None
                    pass
                    
                #except _bt.error as e:
                    #raise BluetoothError(str(e))
                    #my_logger.error(e)  
                    #bleCon.close()
                    #pass
                    #return None
            
        #except Error as e:
            #my_logger.error(e)  
            #return None
        else:
            my_logger.warning("Failed - Bluetooth Connection Socket is Not Avalable: %s", BUID1)
            print ("Failed - Bluetooth Connection Socket is Not Avalable: %s", BUID1)
            return None
            
    else:
        my_logger.warning("Failed - Bluetooth MAC Address is Not Avalable: %s", BUID1)
        print("Failed - Bluetooth MAC Address is Not Avalable: %s", BUID1)
        return None

    '''
    except:
        e = sys.exc_info()[0]
        my_logger.error(e)
        print ("Bluetooth Query Attribute Value not Avalable:",e)

        return None
    '''

#def Query_Tpms_SET_TireID(s):
    

def Query_TpmsTireDataPosition(s, TPMSID1):
    
    #TPMSID1 = TpmsTireDataPosition()
    print binascii.b2a_hex(TPMSID1)
    
    #print "performing Bluetooth Communication..."
    #s.send(TPMSID1)
    
    #while True:
    #s.send(my_hex)
    if(s, TPMSID1 != None):
        
        while(True):
            try:
                s.send(TPMSID1)
        
                time.sleep(1)

                data = s.recv(1024)

                print binascii.b2a_hex(data)
                return data
                break;
                
            except bluetooth.btcommon.BluetoothError as e:
                print "bluetooth.btcommon.BluetoothError",e
                my_logger.error(e)  
                s.close()
                time.sleep(2)
                return None
                pass
    else:
        print ("Bluetooth Send Data Conn, Query TPMSID1 are None:",TPMSID1)
        my_logger.warning("Bluetooth Send Data Conn, Query TPMSID1 are None:",TPMSID1)
        bleCon.close()
        return None
    #if(len(data) == 0):break
    #print binascii.b2a_hex(data)

    #ParseBluetoothTyre(data)
        
        
    print binascii.b2a_hex(data)
        

#    s.close()

#    return data
  


def ParseBluetoothTyre(data):
    
    try:
        if(data != None):
            #hexStr = "aaa14108630006fdaaa1410f630001ba6b09000000002daaa1410f630002ba6d6d0000000094aaa1410f63000356a8cb00000000caaaa1410f63000456a6be00000000bcaaa1410f63000556a7810000000081aaa1410f63000656a7c500000000c6"
            #hexstr = binascii.b2a_hex(data)
            hexstr = data
            
            Tyre1No = hexstr[28:30]
            Tyre1ID = hexstr[30:36]
            Tyre1Presure = hexstr[36:42]
            Tyre1Temp = hexstr[42:44]
            print Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp
            '''
            T = T.append(Tyre1No)
            T = T.apped(Tyre1ID)
            T = T.apped(Tyre1Presure)
            T = T.apped(Tyre1Temp)
            print T
            '''
            Tyre2No = hexstr[58:60]
            Tyre2ID = hexstr[60:66]
            Tyre2Presure = hexstr[66:72]
            Tyre2Temp = hexstr[72:74]
            print Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp

            Tyre3No = hexstr[88:90]
            Tyre3ID = hexstr[90:96]
            Tyre3Presure = hexstr[96:102]
            Tyre3Temp = hexstr[102:104]
            print Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp

            Tyre4No = hexstr[118:120]
            Tyre4ID = hexstr[120:126]
            Tyre4Presure = hexstr[126:132]
            Tyre4Temp = hexstr[132:134]
            print Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp

            Tyre5No = hexstr[148:150]
            Tyre5ID = hexstr[150:156]
            Tyre5Presure = hexstr[156:162]
            Tyre5Temp = hexstr[162:164]
            print Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp

            Tyre6No = hexstr[178:180]
            Tyre6ID = hexstr[180:186]
            Tyre6Presure = hexstr[186:192]
            Tyre6Temp = hexstr[192:194]
            print Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp

            
            print (Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp,Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp,Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp)
            return (Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp,Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp,Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp)
        

        else:
            my_logger.warning("Parse data Not Available")
            return None
        
            
    except:
        e = sys.exc_info()[0]
        my_logger.error(e)
        print ("Bluetooth Parse data Attribute Value not Avalable:",e)

        return None

def fun():
    data = "aaa14108630006fdaaa1410f630001ba6b09000000002daaa1410f630002ba6d6d0000000094aaa1410f63000356a8cb00000000caaaa1410f63000456a6be00000000bcaaa1410f63000556a7810000000081aaa1410f63000656a7c500000000c6"
    hexstr = binascii.b2a_hex(data)

    TPMSID1 = "aa41a1076300f6"
    
    BUID1 = '00:13:EF:C0:02:1E'
    #TpmsTireDataPosition()

    SID1, L1 = "ba6b09", "01"
    SID2, L2 = "ba6b75", "02"
    #Tpms_Tire_SET_Position1(L1, None)
    #Tpms_Tire_SET_Position1(L2, SID2)

    #Tpms_SET_TireID(conn, TMSSET)

    s = connect_ble(BUID1)
    
    #ParseBluetoothTyre(data)

    Query_TpmsTireDataPosition(s, TPMSID1)
    
    

if __name__ == "__main__":  
    
    fun()
