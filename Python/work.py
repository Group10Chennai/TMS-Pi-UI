################################################################
# TPMS Integration -09-2017
################################################################

import serial
import binascii
import sys
import bluetooth
from bluetooth import*
import socket
import time
import sqlite3
from sqlite3 import Error
import __main__
from pip._vendor.pkg_resources import null_ns_handler

import db
import rfid
import blecontroller
from blecontroller import *
import display

import datetime

import glob
import logging
import logging.handlers



#LOG_FILENAME = '/home/pi/Documents/TMS-Git/TMS-Python/log/loggingRotatingFileExample.log'
LOG_FILENAME = '/home/group10/loggingRotatingFileExample.log'

my_logger = logging.getLogger('myapp')
hdlr = logging.FileHandler(LOG_FILENAME)
formatter = logging.Formatter('%(asctime)s :%(levelname)s :%(message)s :')
hdlr.setFormatter(formatter)
my_logger.addHandler(hdlr) 
my_logger.setLevel(logging.DEBUG)



#Variable Decleration
s = 'hello'
data = []
rfidTID_hex = []
rfidTID = []
cksm = []
vehID = 0
vehName = ""
BUID = ""
RFUID = ""
#tag_id = ""

dispVar = ""

tup1=()
_DBSensorID = []
_DBLocation = []

BluetoothSocketVariable= []
DBSensorVariable=[]


#database = "/opt/Aquire/sqlite/TPMS.db"
database = "/opt/JavaServices/sqlite/TPMS.db"
TID1 = "e2000016351702081640767f"
tag_id = "e2000016351702081640767f" #24
#vehID = 32
BUID = '00:13:EF:C0:02:1E' #17



# Start Query the DB with RFID TID
def db_DeviceDetails_by_rfiduid(conn, tag_id):

    try:
        #print("Create a database connection to the DB file .db")
        #conn = db.create_db_connection(database)
        #print tag_id
        #print("Query the database to read Vehicle Details by RFUID")
        #vehDetail = db.select_DeviceDetails_by_rfiduid(conn, "RFID 1")

        if(conn != None): 
            with conn:
                vehDetail = db.select_DeviceDetails_by_rfiduid(conn, tag_id)
                if (vehDetail != None):
                    #Check vehID 
                    if(vehDetail[0] != 0):
                        vehID = vehDetail[0]
                    else:
                        my_logger.warning ("vehID is Not Available", vehDetail[0])
                        
                    #Check vehName
                    if(vehDetail[1] != None):
                        vehName = vehDetail[1].strip()
                    else:
                        my_logger.warning ("vehName is Not Available", vehDetail[1].strip())
                        
                    #Check BUID and Mac Address Length
                    if((vehDetail[2] != None) &(len(vehDetail[2].strip()) == 17)):
                        BUID = vehDetail[2].strip()
                    else:
                        my_logger.warning ("BUID is Not Available", vehDetail[2])
                        
                    #Check RFUID and tagid Length
                    if((vehDetail[3] != None) & (len(vehDetail[3].strip()) == 24)):
                        RFUID = vehDetail[3].strip()
                    else:
                        my_logger.warning ("BUID is Not Available", vehDetail[2])
                        
                    
                    if(vehID, vehName, BUID, RFUID != None):                   
                        my_logger.info ("If vehID : %s, vehName : %s, BUID : %s, RFUID : %s are Available", vehID, vehName, BUID, RFUID)
                        print ("If vehID : %s, vehName : %s, BUID : %s, RFUID : %s are Available", vehID, vehName, BUID, RFUID)
                        #Add Response Class
                        return vehID, vehName, BUID, RFUID
                        #return  vehDetail
                    else:
                        my_logger.warning ("If vehID : %s, vehName : %s, BUID : %s, RFUID : %s  are NONE", vehID, vehName, BUID, RFUID) 
                        #Add Response Class
                        return None                
                else:
                    my_logger.warning ("db.select_DeviceDetails_by_rfiduid vehDetail None : %s." , vehDetail) 
                    #Add Response Class
                    return None
                #print vehID, vehName, BUID, RFUID       
        else:
            my_logger.warning ("Connection to DB is None " )
            return None
    except:
        e = sys.exc_info()[0]
        my_logger.error(e)
        print ("Bluetooth Parse data Attribute Value not Avalable:",e)

        return None
    
'''

# Start Query the DB with vehID to get Tyre Details
def db_DeviceDetails_by_vehID(vehID1):

    print("Create a database connection to the DB file .db")
    conn = db.create_db_connection(database)
    
    #print vehID
    print("Query the database to read Tyre Details by vehID")
    #vehDetail = db.select_DeviceDetails_by_rfiduid(conn, vehID)

    with conn:
        TyreDetail = db.select_TyreDetails_by_VehId(conn, 24)
        #print TyreDetail
    if (TyreDetail != None):

     
        if(TyreDetail[0] != None):
            Tyre_row1 = TyreDetail[0]

            SID1, L1 = Tyre_row1[0], Tyre_row1[1]
            print SID1, L1
            
        if(TyreDetail[1] != None):
            Tyre_row2 = TyreDetail[1]

            SID2, L2 = Tyre_row2[0], Tyre_row2[1]
            print SID2, L2
            
        if(TyreDetail[2] != None):
            Tyre_row3 = TyreDetail[2]

            SID3, L3 = Tyre_row3[0], Tyre_row3[1]
            print SID3, L3

        if(TyreDetail[3] != None):
            Tyre_row4 = TyreDetail[3]

            SID4, L4 = Tyre_row4[0], Tyre_row4[1]
            print SID4, L4

        if(TyreDetail[4] != None):
            Tyre_row5 = TyreDetail[4]

            SID5, L5 = Tyre_row5[0], Tyre_row5[1]
            print SID5, L5

        if(TyreDetail[5] != None):
            Tyre_row6 = TyreDetail[5]

            SID6, L6 = Tyre_row6[0], Tyre_row6[1]
            print SID6, L6
       
        
    
    print("Close a database connection to the DB file .db")
    conn.close()
    
    #return vehID, vehName, BUID, RFUID

'''

# Start Query the DB with vehID to get Tyre Details
# Assign Location  by value
# FL = 01, FR = 02, RLO = 03, RLI = 04, RRI = 05, RRO = 06
def db_DeviceDetails_by_vehID(DBconn, vehID1):

    #print("Create a database connection to the DB file .db")
    #conn = db.create_db_connection(database)
    
    #print vehID
    print("Query the database to read Tyre Details by vehID")
    #vehDetail = db.select_DeviceDetails_by_rfiduid(conn, vehID)
    DBTyreDetail = []

    try:
        
        with DBconn:
            TyreDetail = db.select_TyreDetails_by_VehId(DBconn, vehID1)

            DBtotalTyres = len(TyreDetail)
            print DBtotalTyres

        if TyreDetail is not None:
            for DBi in range(1, DBtotalTyres+1):

                if(DBi == 1):
                    
                    Tyre_row1 = TyreDetail[0]

                    SID1 = Tyre_row1[0]
                    
                    if Tyre_row1[1] == "FL":
                        L1 = "01"
                    elif Tyre_row1[1] == "FR":
                        L1 = "02"
                    elif Tyre_row1[1] == "RLO":
                        L1 = "03"
                    elif Tyre_row1[1] == "RLI":
                        L1 = "04"
                    elif Tyre_row1[1] == "RRI":
                        L1 = "05"
                    elif Tyre_row1[1] == "RRO":
                        L1 = "06"            
                        
                    #print SID1, L1
                    DBTyreDetail.append(SID1)
                    DBTyreDetail.append(L1)
                    
                    if DBi == int(DBtotalTyres):
                        
                        print DBTyreDetail
                        return DBTyreDetail

                elif(DBi == 2):

                    Tyre_row2 = TyreDetail[1]

                    SID2 = Tyre_row2[0]

                    if Tyre_row2[1] == "FL":
                        L2 = "01"
                    elif Tyre_row2[1] == "FR":
                        L2 = "02"
                    elif Tyre_row2[1] == "RLO":
                        L2 = "03"
                    elif Tyre_row2[1] == "RLI":
                        L2 = "04"
                    elif Tyre_row2[1] == "RRI":
                        L2 = "05"
                    elif Tyre_row2[1] == "RRO":
                        L2 = "06"
                        
                    #print SID2, L2
                    DBTyreDetail.append(SID2)
                    DBTyreDetail.append(L2)
                    
                    if DBi == int(DBtotalTyres):
                        
                        print DBTyreDetail
                        return DBTyreDetail

                elif(DBi == 3):

                    Tyre_row3 = TyreDetail[2]

                    SID3 = Tyre_row3[0]

                    if Tyre_row3[1] == "FL":
                        L3 = "01"
                    elif Tyre_row3[1] == "FR":
                        L3 = "02"
                    elif Tyre_row3[1] == "RLO":
                        L3 = "03"
                    elif Tyre_row3[1] == "RLI":
                        L3 = "04"
                    elif Tyre_row3[1] == "RRI":
                        L3 = "05"
                    elif Tyre_row3[1] == "RRO":
                        L3 = "06"
                        
                    #print SID3, L3
                    DBTyreDetail.append(SID3)
                    DBTyreDetail.append(L3)
                    
                    if DBi == int(DBtotalTyres):

                        print DBTyreDetail
                        return DBTyreDetail

                elif(DBi == 4):
                    
                    Tyre_row4 = TyreDetail[3]

                    SID4 = Tyre_row4[0]

                    if Tyre_row4[1] == "FL":
                        L4 = "01"
                    elif Tyre_row4[1] == "FR":
                        L4 = "02"
                    elif Tyre_row4[1] == "RLO":
                        L4 = "03"
                    elif Tyre_row4[1] == "RLI":
                        L4 = "04"
                    elif Tyre_row4[1] == "RRI":
                        L4 = "05"
                    elif Tyre_row4[1] == "RRO":
                        L4 = "06"

                    #print SID4, L4
                    DBTyreDetail.append(SID4)
                    DBTyreDetail.append(L4)
                    
                    if DBi == int(DBtotalTyres):

                        print DBTyreDetail
                        return DBTyreDetail

                elif(DBi == 5):

                    Tyre_row5 = TyreDetail[4]

                    SID5 = Tyre_row5[0]

                    if Tyre_row5[1] == "FL":
                        L5 = "01"
                    elif Tyre_row5[1] == "FR":
                        L5 = "02"
                    elif Tyre_row5[1] == "RLO":
                        L5 = "03"
                    elif Tyre_row5[1] == "RLI":
                        L5 = "04"
                    elif Tyre_row5[1] == "RRI":
                        L5 = "05"
                    elif Tyre_row5[1] == "RRO":
                        L5 = "06"
                        
                    #print SID5, L5                
                    DBTyreDetail.append(SID5)
                    DBTyreDetail.append(L5)
                    
                    if DBi == int(DBtotalTyres):

                        print DBTyreDetail
                        return DBTyreDetail

                elif(DBi == 6):

                    Tyre_row6 = TyreDetail[5]

                    SID6 = Tyre_row6[0]

                    if Tyre_row6[1] == "FL":
                        L6 = "01"
                    elif Tyre_row6[1] == "FR":
                        L6 = "02"
                    elif Tyre_row6[1] == "RLO":
                        L6 = "03"
                    elif Tyre_row6[1] == "RLI":
                        L6 = "04"
                    elif Tyre_row6[1] == "RRI":
                        L6 = "05"
                    elif Tyre_row6[1] == "RRO":
                        L6 = "06"
                        
                    #print SID6, L6
                    DBTyreDetail.append(SID6)
                    DBTyreDetail.append(L6)
                    
                    if DBi == int(DBtotalTyres):

                        print DBTyreDetail
                        return DBTyreDetail

                elif(DBi > 6):
                    my_logger.warning("Failed - DB Select TyreDetails by VehId in DBtotalTyres is more than 6: %s, %s ",DBi, DBtotalTyres)
                    print ("Failed - DB Select TyreDetails by VehId in DBtotalTyres is more than 6:",DBi, DBtotalTyres)
                    return None   
                    

        elif TyreDetail is None:
            my_logger.warning("Failed - DB Select TyreDetails by VehId in TyreDetail is None: %s",TyreDetail)
            print ("Failed - DB Select TyreDetails by VehId in TyreDetail is None:",TyreDetail)
            return None 

    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - DB Select TyreDetails by VehId is not available: %s, %s ",e, VehId)
        print ("Failed - DB Select TyreDetails by VehId is not available:",e, VehId)
        return None
        
        #print("Close a database connection to the DB file .db")
        #DBconn.close()
    

# Start Connecting the Socket by BUID
def Connect_Socket_Bluetooth_by_BUID( conn):

    #print("Create a Bluetooth connection")
    #conn = blecontroller.connect_ble(BUID)
   
    #blecontroller.Tpms_Tire_SET_Position1(SID1, L1)
    #print("Query the Bluetooth Controller to set TyreNo, Sensor ID")
    #data = blecontroller.Query_Tpms_SET_TireID(conn)
    if(conn != None):
        try:
            print("Query the Bluetooth Controller with 63 to read All TyreNo, Sensor ID, Pressure and Temp")
            TPMSID1 = blecontroller.TpmsTireDataPosition()

            if(TPMSID1 != None):
            
                print("Query the Bluetooth Controller to read TyreNo, Sensor ID, Pressure and Temp")
                data = blecontroller.Query_TpmsTireDataPosition(conn, TPMSID1)

                if(data != None):

                    print("Parse the hex data string TyreNo, Sensor ID, Pressure and Temp")    
                    
                    BluetoothSocketVariable1 = blecontroller.ParseBluetoothTyre(data)

                    #print BluetoothSocketVariable1

                    return BluetoothSocketVariable1
                
                else:
                    my_logger.warning("Failed - BT Query Data not Available from the Bluetooth Controller: %s ", data)
                    print ("Failed - BT Query Data not Available from the Bluetooth Controller:", data)
                    return None
            else:
                my_logger.warning("Failed - BT Query the Bluetooth Controller with 63 to read All is None: %s, %s ",e, TPMSID1)
                print ("Failed - BT Query the Bluetooth Controller with 63 to read All is None:",e, TPMSID1)
                return None
            
        except:
            e = sys.exc_info()[0]
            my_logger.error("Failed - BT Query the Bluetooth Controller with 63 to read All is None: %s, %s ",e, TPMSID1)
            print ("Failed - BT Query the Bluetooth Controller with 63 to read All is None:",e, TPMSID1)
            return None
    else:
        my_logger.warning("Failed - BT Query the Bluetooth Controller BTConnection is None: %s",conn)
        print ("Failed - BT Query the Bluetooth Controller BTConnection is None:",conn)
        return None
    
    #print("Compare DB Sensor UID, tirePosition with Bluetooth TyreNo, TyreID")

    #compare_DBSensorUID_DBLocation_BTyreNo_BTyreID()

    
# Start Configuring the Bluetooth Controller Based on the DB Parameters   
def configure_BTController(bleConn, DBSensorVariable):

    try:

        print "DBSensorVariable", DBSensorVariable

        for i in range(0,len(DBSensorVariable),2):

            #Check 01 Location and Related Sensor ID
            
            #print "in DBSensorVariable[i] ",( DBSensorVariable[i+1], DBSensorVariable[i])

            #print "BluetoothSocketVariable SensorID Not Assigned"
            RetValConf = assignNewSensorToBTC(bleConn, DBSensorVariable[i+1], DBSensorVariable[i])
            time.sleep(0.3)
            
            if RetValConf == "aa":
                continue
            else:
                my_logger.warning("Failed - BT Query the Bluetooth Controller to configure Sensor ID, Location - RetValConf is None or FF: %s, %s, %s",DBSensorVariable[i+1], DBSensorVariable[i], RetValConf)
                print ("Failed - BT Query the Bluetooth Controller to configure Sensor ID, Location - RetValConf is None or FF: ",DBSensorVariable[i+1], DBSensorVariable)
                #return None

            
    
    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Bluetooth Query Attribute to Set (Location, Sensor ID) None:%s, %s ",e)
        print ("Failed - Bluetooth Query Attribute to Set (Location, Sensor ID) None: ",e)

        return None

           
def compare_DBSensorUID_DBLocation_BTyreNo_BTyreID(conn, DBSensorVariable, BluetoothSocketVariable):

    print DBSensorVariable
    print BluetoothSocketVariable
    
    BTtotalTyres = int(BluetoothSocketVariable[0])
    print "Total Tyres:", BTtotalTyres

    if (DBSensorVariable is not None) and (BluetoothSocketVariable is not None):

        #Check the DBSensorVariable and find the DBSensorID, DBLocation 
        for i in range(len(DBSensorVariable)):

            #Check 01 Location and Related Sensor ID
            if(DBSensorVariable[i] == "01"):
                _DBSensorID1 =  DBSensorVariable[i-1]
                _DBLocation1 =  DBSensorVariable[i]
                print "in DBSensorVariable[i] ",_DBLocation1, _DBSensorID1
                
            #Check 02 Location and Related Sensor ID
            if(DBSensorVariable[i] == "02"):
                _DBSensorID2 =  DBSensorVariable[i-1]
                _DBLocation2 =  DBSensorVariable[i]
                print "in DBSensorVariable[i] ",_DBLocation2, _DBSensorID2

            #Check 03 Location and Related Sensor ID
            if(DBSensorVariable[i] == "03"):
                _DBSensorID3 =  DBSensorVariable[i-1]
                _DBLocation3 =  DBSensorVariable[i]
                print "in DBSensorVariable[i] ",_DBLocation3, _DBSensorID3

            #Check 04 Location and Related Sensor ID
            if(DBSensorVariable[i] == "04"):
                _DBSensorID4 =  DBSensorVariable[i-1]
                _DBLocation4 =  DBSensorVariable[i]
                print "in DBSensorVariable[i] ",_DBLocation4, _DBSensorID4

            #Check 05 Location and Related Sensor ID
            if(DBSensorVariable[i] == "05"):
                _DBSensorID5 =  DBSensorVariable[i-1]
                _DBLocation5 =  DBSensorVariable[i]
                print "in DBSensorVariable[i] ",_DBLocation5, _DBSensorID5

            #Check 06 Location and Related Sensor ID
            if(DBSensorVariable[i] == "06"):
                _DBSensorID6 =  DBSensorVariable[i-1]
                _DBLocation6 =  DBSensorVariable[i]
                print "in DBSensorVariable[i] ",_DBLocation6, _DBSensorID6

    
    
        #Check the BluetoothSocketVariable and find the BTSensorID, BTLocation    
        for v in range(len(BluetoothSocketVariable)):

            if(BluetoothSocketVariable[v] == "01"):

                _BTLocation1 = BluetoothSocketVariable[v]
                _BTSensorID1 = BluetoothSocketVariable[v+1]
                print "in BluetoothSocketVariable[v] ",_BTLocation1, _BTSensorID1

            if(BluetoothSocketVariable[v] == "02"):
                        
                _BTLocation2 = BluetoothSocketVariable[v]
                _BTSensorID2 = BluetoothSocketVariable[v+1]
                print "in BluetoothSocketVariable[v] ",_BTLocation2, _BTSensorID2

            if(BluetoothSocketVariable[v] == "03"):
                        
                _BTLocation3 = BluetoothSocketVariable[v]
                _BTSensorID3 = BluetoothSocketVariable[v+1]
                print "in BluetoothSocketVariable[v] ",_BTLocation3, _BTSensorID3

            if(BluetoothSocketVariable[v] == "04"):
                        
                _BTLocation4 = BluetoothSocketVariable[v]
                _BTSensorID4 = BluetoothSocketVariable[v+1]
                print "in BluetoothSocketVariable[v] ",_BTLocation4, _BTSensorID4

            if(BluetoothSocketVariable[v] == "05"):
                        
                _BTLocation5 = BluetoothSocketVariable[v]
                _BTSensorID5 = BluetoothSocketVariable[v+1]
                print "in BluetoothSocketVariable[v] ",_BTLocation5, _BTSensorID5

            if(BluetoothSocketVariable[v] == "06"):
                        
                _BTLocation6 = BluetoothSocketVariable[v]
                _BTSensorID6 = BluetoothSocketVariable[v+1]
                print "in BluetoothSocketVariable[v] ",_BTLocation6, _BTSensorID6

        
                
        #Compare Sensor ID and location 
        for i in range(len(DBSensorVariable)):
            
            for v in range(len(BluetoothSocketVariable)):                  
            
                #Check 01 Location and Related Sensor ID
                if(DBSensorVariable[i] == "01"):
                    _DBSensorID1 =  DBSensorVariable[i-1]
                    _DBLocation1 =  DBSensorVariable[i]

                    if(BluetoothSocketVariable[v] == "01"):
                        #print "in BluetoothSocketVariable[v] ",_DBLocation1, _DBSensorID1

                        _BTLocation1 = BluetoothSocketVariable[v]
                        _BTSensorID1 = BluetoothSocketVariable[v+1]
                        #print "in BluetoothSocketVariable[v] ",_BTLocation1, _BTSensorID1
                        
                        if(BluetoothSocketVariable[v+1] != None):
                            
                            if(_DBSensorID1 == BluetoothSocketVariable[v+1]):
                                #print "in if ", _BTLocation1, _BTSensorID1
                                print ("BTSensorID1 and DBSensorID1 are Same", _BTSensorID1, _DBSensorID1)
                                continue
                            elif (_DBSensorID1 != BluetoothSocketVariable[v+1]):
                                #print "in else ", _BTLocation1, _BTSensorID1
                                print ("BTSensorID1 and DBSensorID1 are Not Same", _BTSensorID1, _DBSensorID1)
                                RetVal = assignNewSensorToBTC(conn, _DBLocation1, _DBSensorID1)

                                if RetVal is "aa":
                                    continue
                                else:
                                    return None
                        else:
                            print "BluetoothSocketVariable SensorID Not Assigned"
                            assignNewSensorToBTC(conn, _DBLocation1, _DBSensorID1)
                        
                    elif (BluetoothSocketVariable[v] == None):
                        #print "in None",_BTLocation1, _BTSensorID1
                        assignNewSensorToBTC(conn, _DBLocation1, _DBSensorID1)


                #Check 02 Location and Related Sensor ID
                if(DBSensorVariable[i] == "02"):
                    _DBSensorID2 =  DBSensorVariable[i-1]
                    _DBLocation2 =  DBSensorVariable[i]

                    if(BluetoothSocketVariable[v] == "02"):
                        #print "in BluetoothSocketVariable[v] ",_DBLocation2, _DBSensorID2

                        _BTLocation2 = BluetoothSocketVariable[v]
                        _BTSensorID2 = BluetoothSocketVariable[v+1]
                        #print "in BluetoothSocketVariable[v] ",_BTLocation2, _BTSensorID2
                        
                        if(BluetoothSocketVariable[v+1] != None):
                            
                            if(_DBSensorID2 == BluetoothSocketVariable[v+1]):
                                #print "in if ", _BTLocation2, _BTSensorID2
                                print ("BTSensorID2 and DBSensorID2 are Same", _BTSensorID2, _DBSensorID2)
                                continue
                            elif (_DBSensorID2 != BluetoothSocketVariable[v+1]):
                                #print "in else ", _BTLocation2, _BTSensorID2
                                print ("BTSensorID2 and DBSensorID2 are Not Same", _BTSensorID2, _DBSensorID2)
                                RetVal = assignNewSensorToBTC(conn, _DBLocation2, _DBSensorID2)

                                if RetVal is "aa":
                                    continue
                                else:
                                    return None
                        else:
                            print "BluetoothSocketVariable SensorID Not Assigned"
                            assignNewSensorToBTC(conn, _DBLocation2, _DBSensorID2)
                        
                    elif (BluetoothSocketVariable[v] == None):
                        #print "in None",_BTLocation2, _BTSensorID2
                        assignNewSensorToBTC(conn, _DBLocation2, _DBSensorID2)
                        

                #Check 03 Location and Related Sensor ID
                if(DBSensorVariable[i] == "03"):
                    _DBSensorID3 =  DBSensorVariable[i-1]
                    _DBLocation3 =  DBSensorVariable[i]

                    if(BluetoothSocketVariable[v] == "03"):
                        #print "in BluetoothSocketVariable[v] ",_DBLocation3, _DBSensorID3

                        _BTLocation3 = BluetoothSocketVariable[v]
                        _BTSensorID3 = BluetoothSocketVariable[v+1]
                        #print "in BluetoothSocketVariable[v] ",_BTLocation3, _BTSensorID3
                        
                        if(BluetoothSocketVariable[v+1] != None):
                            
                            if(_DBSensorID3 == BluetoothSocketVariable[v+1]):
                                #print "in if ", _BTLocation3, _BTSensorID3
                                print ("BTSensorID3 and DBSensorID3 are Same", _BTSensorID3, _DBSensorID3)
                                continue
                            elif (_DBSensorID3 != BluetoothSocketVariable[v+1]):
                                #print "in else ", _BTLocation3, _BTSensorID3
                                print ("BTSensorID3 and DBSensorID3 are Not Same", _BTSensorID3, _DBSensorID3)
                                RetVal = assignNewSensorToBTC(conn, _DBLocation3, _DBSensorID3)

                                if RetVal is "aa":
                                    continue
                                else:
                                    return None
                        else:
                            print "BluetoothSocketVariable SensorID Not Assigned"
                            assignNewSensorToBTC(conn, _DBLocation3, _DBSensorID3)
                        
                    elif (BluetoothSocketVariable[v] == None):
                        #print "in None",_BTLocation3, _BTSensorID3
                        assignNewSensorToBTC(conn, _DBLocation3, _DBSensorID3)


                #Check 04 Location and Related Sensor ID
                if(DBSensorVariable[i] == "04"):
                    _DBSensorID4 =  DBSensorVariable[i-1]
                    _DBLocation4 =  DBSensorVariable[i]

                    if(BluetoothSocketVariable[v] == "04"):
                        #print "in BluetoothSocketVariable[v] ",_DBLocation4, _DBSensorID4

                        _BTLocation4 = BluetoothSocketVariable[v]
                        _BTSensorID4 = BluetoothSocketVariable[v+1]
                        #print "in BluetoothSocketVariable[v] ",_BTLocation4, _BTSensorID4
                        
                        if(BluetoothSocketVariable[v+1] != None):
                            
                            if(_DBSensorID4 == BluetoothSocketVariable[v+1]):
                                #print "in if ", _BTLocation4, _BTSensorID4
                                print ("BTSensorID4 and DBSensorID4 are Same", _BTSensorID4, _DBSensorID4)
                                continue
                            elif (_DBSensorID4 != BluetoothSocketVariable[v+1]):
                                #print "in else ", _BTLocation4, _BTSensorID4
                                print ("BTSensorID4 and DBSensorID4 are Not Same", _BTSensorID4, _DBSensorID4)
                                RetVal = assignNewSensorToBTC(_conn, DBLocation4, _DBSensorID4)

                                if RetVal is "aa":
                                    continue
                                else:
                                    return None
                        else:
                            print "BluetoothSocketVariable SensorID Not Assigned"
                            assignNewSensorToBTC(conn, _DBLocation4, _DBSensorID4)
                        
                    elif (BluetoothSocketVariable[v] == None):
                        #print "in None",_BTLocation4, _BTSensorID4
                        assignNewSensorToBTC(conn, _DBLocation4, _DBSensorID4)
                        

                #Check 05 Location and Related Sensor ID
                if(DBSensorVariable[i] == "05"):
                    _DBSensorID5 =  DBSensorVariable[i-1]
                    _DBLocation5 =  DBSensorVariable[i]

                    if(BluetoothSocketVariable[v] == "05"):
                        #print "in BluetoothSocketVariable[v] ",_DBLocation5, _DBSensorID5

                        _BTLocation5 = BluetoothSocketVariable[v]
                        _BTSensorID5 = BluetoothSocketVariable[v+1]
                        #print "in BluetoothSocketVariable[v] ",_BTLocation5, _BTSensorID5
                        
                        if(BluetoothSocketVariable[v+1] != None):
                            
                            if(_DBSensorID5 == BluetoothSocketVariable[v+1]):
                                #print "in if ", _BTLocation5, _BTSensorID5
                                print ("BTSensorID5 and DBSensorID5 are Same", _BTSensorID5, _DBSensorID5)
                                continue
                            elif (_DBSensorID5 != BluetoothSocketVariable[v+1]):
                                #print "in else ", _BTLocation5, _BTSensorID5
                                print ("BTSensorID5 and DBSensorID5 are Not Same", _BTSensorID5, _DBSensorID5)
                                RetVal = assignNewSensorToBTC(conn, _DBLocation5, _DBSensorID5)

                                if RetVal is "aa":
                                    continue
                                else:
                                    return None
                        else:
                            print "BluetoothSocketVariable SensorID Not Assigned"
                            assignNewSensorToBTC(conn, _DBLocation5, _DBSensorID5)
                        
                    elif (BluetoothSocketVariable[v] == None):
                        #print "in None",_BTLocation5, _BTSensorID5
                        assignNewSensorToBTC(conn, _DBLocation5, _DBSensorID5)


                #Check 06 Location and Related Sensor ID
                if(DBSensorVariable[i] == "06"):
                    _DBSensorID6 =  DBSensorVariable[i-1]
                    _DBLocation6 =  DBSensorVariable[i]

                    if(BluetoothSocketVariable[v] == "06"):
                        #print "in BluetoothSocketVariable[v] ",_DBLocation6, _DBSensorID6

                        _BTLocation6 = BluetoothSocketVariable[v]
                        _BTSensorID6 = BluetoothSocketVariable[v+1]
                        #print "in BluetoothSocketVariable[v] ",_BTLocation6, _BTSensorID6
                        
                        if(BluetoothSocketVariable[v+1] != None):
                            
                            if(_DBSensorID6 == BluetoothSocketVariable[v+1]):
                                #print "in if ", _BTLocation6, _BTSensorID6
                                print ("BTSensorID6 and DBSensorID6 are Same", _BTSensorID6, _DBSensorID6)
                                continue
                            elif (_DBSensorID6 != BluetoothSocketVariable[v+1]):
                                #print "in else ", _BTLocation6, _BTSensorID6
                                print ("BTSensorID6 and DBSensorID6 are Not Same", _BTSensorID6, _DBSensorID6)
                                RetVal = assignNewSensorToBTC(conn, _DBLocation6, _DBSensorID6)

                                if RetVal is "aa":
                                    continue
                                else:
                                    return None
                        else:
                            #print "BluetoothSocketVariable SensorID Not Assigned"
                            print ("BTSensorID6 and DBSensorID6 are Not Same", _BTSensorID6, _DBSensorID6)
                            assignNewSensorToBTC(conn, _DBLocation6, _DBSensorID6)
                        
                    elif (BluetoothSocketVariable[v] == None):
                        #print "in None",_BTLocation6, _BTSensorID6
                        assignNewSensorToBTC(conn, _DBLocation6, _DBSensorID6)


        #Check the Missed tyre form BluetoothSocketVariable
        MissedTyre = [i for i in DBSensorVariable if i not in BluetoothSocketVariable]

        #print MissedTyre

        if MissedTyre is not None:
            
            for BTtyre in MissedTyre:
                
                if BTtyre == "01":
                    print "assignNewSensorToBTC(conn, _DBLocation1, _DBSensorID1)"
                    RetVal = assignNewSensorToBTC(conn, _DBLocation1, _DBSensorID1)
                    
                    if RetVal is "aa":
                        continue
                    else:
                        return None
                    
                elif BTtyre == "02":
                    print "assignNewSensorToBTC(conn, _DBLocation2, _DBSensorID2)"
                    RetVal = assignNewSensorToBTC(conn, _DBLocation2, _DBSensorID2)
                    
                    if RetVal is "aa":
                        continue
                    else:
                        return None
                    
                elif BTtyre == "03":
                    print "assignNewSensorToBTC(conn, _DBLocation3, _DBSensorID3)"
                    RetVal = assignNewSensorToBTC(conn, _DBLocation3, _DBSensorID3)
                    
                    if RetVal is "aa":
                        continue
                    else:
                        return None
                    
                elif BTtyre == "04":
                    print "assignNewSensorToBTC(conn, _DBLocation4, _DBSensorID4)"
                    RetVal = assignNewSensorToBTC(conn, _DBLocation4, _DBSensorID4)
                    
                    if RetVal is "aa":
                        continue
                    else:
                        return None
                    
                elif BTtyre == "05":
                    print "assignNewSensorToBTC(conn, _DBLocation5, _DBSensorID5)"
                    RetVal = assignNewSensorToBTC(conn, _DBLocation5, _DBSensorID5)
                    
                    if RetVal is "aa":
                        continue
                    else:
                        return None

                elif BTtyre == "06":
                    print "assignNewSensorToBTC(conn, _DBLocation6, _DBSensorID6)"
                    RetVal = assignNewSensorToBTC(conn, _DBLocation6, _DBSensorID6)

                    if RetVal is "aa":
                        continue
                    else:
                        return None

        
                  
    
    #print DBSensorVariable[0]
    #print BluetoothSocketVariable[0]
    
    else:
        print ("Failed - Bluetooth and DB Sensor Variable are None:",DBSensorVariable, BluetoothSocketVariable)
        my_logger.warning("Failed - Bluetooth DB Sensor Variable are None: %s %s",DBSensorVariable, BluetoothSocketVariable)
        #return None

def assignNewSensorToBTC(conn, location, sensorUID):

    print ("assignNewSensorToBTC", location, sensorUID)
    
    try:
        if(conn != None):
            if(location is not None) and (sensorUID is not None):
            
                TPMSET = blecontroller.Tpms_Tire_SET_Position1(location, sensorUID)

                if(TPMSET != None):
                    
                    print("Query the Bluetooth Controller to set TyreNo, Sensor ID")
                    data = blecontroller.Tpms_SET_TireID(conn, TPMSET)
                    #conn.close()
                    #print data
                    return data

                else:
                    my_logger.warning("Failed - Bluetooth Query to Send and Receive Command Not Available: %s",TMSSET)
                    print("Failed - Bluetooth Query to Send and Receive Command Not Available: %s",TMSSET)
                    return None
            else:
                my_logger.warning("Failed - Bluetooth Query to assignNewSensorToBTC(Location, Sensor ID) not Avalable: %s, %s",location, sensorUID)
                print ("Failed - Bluetooth Query to assignNewSensorToBTC(Location, Sensor ID) not Avalable: ",location, sensorUID)
                return None
        else:
            
            my_logger.warning("Failed - Bluetooth Connection Socket is Not Avalable: %s", BUID)
            print ("Failed - Bluetooth Connection Socket is Not Avalable: %s", BUID)
            return None


    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Bluetooth Query Attribute to Set (Location, Sensor ID) None:%s, %s, %s ",e, location, sensorUID )
        print ("Failed - Bluetooth Query Attribute to Set (Location, Sensor ID) None: ",e, location, sensorUID )

        return None
                
rows = 8
columns= 16
mylist = [['0' for x in range(columns)] for x in range(rows)]

vehID = 0
vehName = ""
BUID = ""
RFUID = ""
dbConn = ""

dispCommand = "Sarojini Nagar Depot"

#function for java
def javaFun_start(tag_id):
    tag_id1 = tag_id
    print tag_id1

def javaFun_end():
    tag_id1 = None
    print tag_id1

def fun():
    print("Main Function")
    
    try:
        #print("RFID Module Read TAG ID Function")
        #tag_id = rfid.RFIDUHFQueryTag()

        #if tag_id1 != None:
            #tag_id = tag_id1
        #else:
            #print("RFID Module Read TAG ID Function")
            #tag_id = rfid.RFIDUHFQueryTag()
        
    
        if(tag_id != None):
            print("Create a database connection to the DB file .db")
            if(database!=None):
                dbConn = db.create_db_connection(database)
                
                if(dbConn != None):
                    #vehID, vehName, BUID, RFUID = db_DeviceDetails_by_rfiduid(dbConn, tag_id)
                    vehDetails = db_DeviceDetails_by_rfiduid(dbConn, tag_id)
                    #print("Create a database connection to the DB file--- ", vehDetails)
                    
                    if(vehDetails != None):
                        print("Query the Database to read Tyre Details, Sensor ID, Position by vehID")

                        vehID = vehDetails[0]
                        vehName = vehDetails[1]
                        BUID = vehDetails[2]
                        RFUID = vehDetails[3]


                        #Query DB DeviceDetail in VehDetails Table to read vehID, vehName, BUID, RFUID
                        if(vehID != None):
                            print dbConn
                            DBSensorVariable = db_DeviceDetails_by_vehID(dbConn, vehID)                        

                            #print DBSensorVariable
                            #dbConn.close()
                        else:
                            my_logger.warning ("Vehicle ID not Available or None Function :%s ", vehID)
                    else:
                       my_logger.warning ("RFID Tag ID is not available in DB :%s ", tag_id)
                else:
                    my_logger.warning ("No DB Connection ")
            else: 
                my_logger.warning ("Database path Not Available ")
        #else:
            #my_logger.warning ("RFID Tag ID is not available in DB %s: ", tag_id)


            #Query DB Device Detail to read vehID, vehName, BUID, RFUID
            if (BUID != None):
                print("Connect socket RFCOMM to Bluetooth Controller by BUID")                 
                print("Create a Bluetooth connection")
                bleConn = blecontroller.connect_ble(BUID)
                            
                if(bleConn != None):                           
                                

                    if(( DBSensorVariable != None)):
                        print("Configure BT SensorUID, tirePosition based on DB ")

                        RetValCompare = configure_BTController(bleConn, DBSensorVariable)
                                    
                    else:
                        my_logger.warning ("DBSensorVariable  not Available or None Function : %s", DBSensorVariable)


                    mylist = Connect_Socket_Bluetooth_by_BUID(bleConn)
                    

                    #Current date and time
                    #t = datetime.utcnow()
                    #date_time = time.strftime('%H:%M:%S %d/%m/%Y')
                    date_time = int(datetime.datetime.now().strftime("%s")) * 1000
                    print date_time
                    
                    if mylist != None:

                        print("displayLEDBoard ")
                        #Display this data in LED Display with Commands 
                        dispVar = display.displayLEDBoardParameters(mylist)
                        print dispVar
                        
                        #display.displayLEDBoard(vehName, dispCommand, date_time, dispVar)
                        display.displayLEDBoard(vehName, dispCommand, date_time, dispVar)

                        #dbConn = db.create_db_connection(database)
                        with dbConn: 
                               
                            db.update_Latest_data_by_VehId(dbConn, int(vehID), date_time, mylist)

                        dbConn.close()
                                
    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Main Function Crashed:%s ",e)
        print ("Failed - Main Function Crashed: ",e)

        return ("Failed - Main Function Crashed:%s ",e)
    
        '''               
        #Query DB Device Detail to read vehID, vehName, BUID, RFUID
        if (BUID != None):
            print("Connect socket RFCOMM to Bluetooth Controller by BUID")                 
            print("Create a Bluetooth connection")
            bleConn = blecontroller.connect_ble(BUID)
            
            if(bleConn != None):                           
                BluetoothSocketVariable = Connect_Socket_Bluetooth_by_BUID(bleConn)

                #print BluetoothSocketVariable

                if(( DBSensorVariable != None) and (BluetoothSocketVariable != None)):
                    print("Compare DB Sensor UID, tirePosition with Bluetooth TyreNo, TyreID")

                    RetValCompare = compare_DBSensorUID_DBLocation_BTyreNo_BTyreID(bleConn, DBSensorVariable, BluetoothSocketVariable)
                else:
                    my_logger.warning ("DBSensorVariable and BluetoothSocketVariable not Available or None Function : %s %s", DBSensorVariable, BluetoothSocketVariable)
            else:
                my_logger.warning ("Bluetooth ID not connected or Host Not Available or None Function : ")
        else:
            my_logger.warning ("Bluetooth ID not Available or None Function : %s", BUID)
          
        #Query DB Device Detail to read vehID, vehName, BUID, RFUID
        if RetValCompare is not None:
            BluetoothSocketVariableFinal = Connect_Socket_Bluetooth_by_BUID(bleConn)    
            print BluetoothSocketVariableFinal
        ''



    
    update_Latest_data_by_VehId(conn, 2, '2015-01-04', '2015-01-06',2)
    
           
    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Main Function Crashed:%s ",e)
        print ("Failed - Main Function Crashed: ",e)

        return None
    '''
   
    
       
    #DBSensorVariable = (u'SensorUID 15', '01', u'SensorUID 14', '02', u'SensorUID 22', '03', u'SensorUID 21', '04', u'SensorUID 20', '06', u'SensorUID 19', '05')
    #DBSensorVariable = (u'ba6b09', '01', u'ba6d6d', '02', u'56a8cb', '03', u'56a6be', '04', u'56a781', '05', u'56a7c5', '06')
    #BluetoothSocketVariable = ('01', 'ba6b09', '000000', '00', '02', 'ba6d6d', '000000', '00', '03', '56a8cb', '000000', '00', '04', '56a6be', '000000', '00', '05', '56a781', '000000', '00', '06', '56a7c5', '000000', '00')
    #DBSensorVariable = (u'ba6b09', '01', u'56a8cb', '03', u'ba6d6d', '02', u'56a6be', '04', u'56a781', '06', u'56a7c5', '05')
    #BluetoothSocketVariable = (5, '01', 'ba6b09', '000000', '00', '02', 'ba6d6d', '000000', '00', '03', '56a8cb', '000000', '00', '04', '56a6be', '000000', '00', '05', '56a781', '000000', '00')
    #BluetoothSocketVariable = ( )
    #compare_DBSensorUID_DBLocation_BTyreNo_BTyreID(DBSensorVariable, BluetoothSocketVariable)
    
    #print("After While Loop Connect socket RFCOMM to Bluetooth Controller by BUID")
    #bleConn.close()

import threading
if __name__ == "__main__":  
    

    #def printit():
        #threading.Timer(5.0, printit).start()
        #print "Hello, World!"
        #fun()
    #printit()

    fun()
    
        
