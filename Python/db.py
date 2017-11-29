###############################################################
# TMS Database Connection File
###############################################################

import sqlite3
from sqlite3 import Error
import __main__
from pip._vendor.pkg_resources import null_ns_handler
 
import glob
import logging
import logging.handlers

import time


LOG_FILENAME = '/home/pi/Documents/TMS-Git/TMS-Python/log/loggingRotatingFileExample.log'
'''
# Set up a specific logger with our desired output level
#LOG_FILENAME = 'example.log'
my_logger= logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
#my_logger = logging.getLogger('MyLogger')
#my_logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=20, backupCount=1)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

my_logger.setFormatter(formatter)

my_logger.addHandler(handler)



my_logger = logging.basicConfig(format='%(asctime)s :%(levelname)s: %(message)s',filename=LOG_FILENAME,level=logging.DEBUG)
my_logger = logging.getLogger('MyLogger')
'''


my_logger = logging.getLogger('myapp')
hdlr = logging.FileHandler(LOG_FILENAME)
formatter = logging.Formatter('%(asctime)s :%(levelname)s :%(message)s :')
hdlr.setFormatter(formatter)
my_logger.addHandler(hdlr) 
my_logger.setLevel(logging.DEBUG)


#def create database connection
def create_db_connection(db_file):
    """Create a database connection to the DB file .db"""
    
    try:
        conn = sqlite3.connect(db_file)
        my_logger.info(" Create a connection to DB ")
        return conn
    except sqlite3.Error as e:
        print ("Failed - Create a connection to DB to the path: ", db_file)
        my_logger.error("Failed - Create a connection to DB to the path: %s", db_file)
        #raise
        return None


    

#Query DB Select Deveice detail by rfiduid
def select_DeviceDetails_by_rfiduid(conn, rfiduid1):
    """
    Query tasks by rfiduid
    param conn: the Connection object
    param rfiduid:
    """
    
    if(rfiduid1 != None):
    #print (" DB select_DeviceDetails_by_id")
    #my_logger.info(" DB select_DeviceDetails_by_id")
        try:
            cur = conn.cursor()
            cur.execute("SELECT vehId, vehName, BUID, RFUID FROM DeviceDetails WHERE RFUID=?",(rfiduid1,))
 
            rows = cur.fetchall()
            vehDetails = None;
            for row in rows:
                if(row != None):
                    vehDetails = row
                    print vehDetails
            if (vehDetails != None):
                
                return vehDetails
            else:
                print ("Failed - Accessing to DB table DeviceDetails by RFID UID - Not Available: ",rfiduid1)
                my_logger.warning("Failed - Accessing to DB table DeviceDetails by RFID UID - Not Available: %d",(rfiduid1))
                
                return None
    
        except sqlite3.Error as e:
            print ("Failed - Accessing to DB table DeviceDetails by RFID UID - Not Available: ",rfiduid1)
            my_logger.error("Failed - Accessing to DB table DeviceDetails by RFID UID - Not Available:  %d, %d ",e, rfiduid1)
            #raise
            return None
    else:
        print ("FFailed - Accessing to DB table DeviceDetails by RFID UID - None: ",rfiduid1)
        my_logger.warning("Failed - Accessing to DB table DeviceDetails by RFID UID - None: %s",(rfiduid1))
                
        return None
    

def select_TyreDetails_by_VehId(conn, VehId1):
    """
    Query tasks by priority
    param conn: the Connection object
    param rfiduid:
    """
    
    if(VehId1 != None):
        
        TyreDetials = []
        #my_logger.info (" DB select_TireDetails_by_VehId ")
        try:
            cur = conn.cursor()
            cur.execute("SELECT sensorUID, tirePosition FROM TireDetails WHERE vehId=?",(VehId1,))
            
            rows = cur.fetchall()
            TyreDetails = None;
            for row in rows:
                TyreDetails = row
                #print TyreDetails
        
            #return TyreDetials
            #return rows

            if (len(rows) != 0):
                #print len(rows)
                #print rows
                return rows
            else:
                print ("Failed - Accessing to DB table TyreDetails by Vehicle ID - Not Available: ",VehId1)
                my_logger.warning("Failed - Accessing to DB table TyreDetails by Vehicle ID - Not Available: %d",(VehId1))
                
                return None
    
        except sqlite3.Error as e:
            print ("Failed - Accessing to DB table TyreDetails by Vehicle ID - Not Available: ",VehId1)
            my_logger.error("Failed - sqlite3.Error and Accessing to DB table TyreDetails by Vehicle ID - Not Available: %d, %d ",e, VehId1)
            #raise
            #conn.close()
            return None
    else:
        print ("Failed - Accessing to DB table TyreDetails by Vehicle ID - None: ",VehId1)
        my_logger.warning("Failed - Accessing to DB table TyreDetails by Vehicle ID - None %s",(VehId1))
                
        return None

'''
def update_Latest_data_by_VehId(conn, vehId1, BTVar):
    #pass vehId and get the data from Latest_data table 
    # If latest data is none - means data not exists -> Need to insert
    # If latest data is not none - means data exists -> Need to update

    #for i in range(len(BTVar)):
        #print BTVar[i]

    #BluetoothSocketVariable = ('01', 'ba6b09', '000000', '00', '02', 'ba6d6d', '000000', '00', '03', '56a8cb', '000000', '00', '04', '56a6be', '000000', '00', '05', '56a781', '000000', '00', '06', '56a7c5', '000000', '00')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Latest_data WHERE vehId=?",(vehId1,))
            
    rows = cur.fetchall()
    print rows
    if len(rows) == 0:

        sql = '' INSERT INTO Latest_data (vehId, device_date_time,
                    FLS, FLP, FLT,
                    FRS, FRP, FRT,
                    RLOS, RLOP, RLOT,
                    RLIS, RLIP, RLIT,
                    RRIS, RRIP, RRIT,
                    RROS, RROP, RROT, count, status)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''

        #queryParam = (vehId1, 125368547, FLS, FLP, FLT, FRS, FRP, FRT, RLOS, RLOP, RLOT, RLIS, RLIP, RLIT, RRIS, RRIP, RRIT, RROS, RROP, RROT, 1, 0)
        queryParam = (vehId1, 125368547, BTVar[1], BTVar[2], BTVar[3], BTVar[5], BTVar[6], BTVar[7], BTVar[9], BTVar[10], BTVar[11], BTVar[13], BTVar[14], BTVar[15], BTVar[17], BTVar[18], BTVar[19], BTVar[21], BTVar[22], BTVar[23], 1, 0)
        cur = conn.cursor()
        cur.execute(sql, queryParam)
        print "Need to insert"

    else:

        sql = '' UPDATE Latest_data SET
                device_date_time = ? ,
                FLS = ? , FLP = ? , FLT = ? ,
                FRS = ? , FRP = ? , FRT = ? ,
                RLOS = ? , RLOP = ? , RLOT = ? ,
                RLIS = ? , RLIP = ? , RLIT = ? ,
                RRIS = ? , RRIP = ? , RRIT = ? ,
                RROS = ? , RROP = ? , RROT = ?, count = ?, status = ? 
                WHERE vehId = ?''
        print "Need to update"
    
        queryParam = (000000000, BTVar[1], BTVar[2], BTVar[3], BTVar[5], BTVar[6], BTVar[7], BTVar[9], BTVar[10], BTVar[11], BTVar[13], BTVar[14], BTVar[15], BTVar[17], BTVar[18], BTVar[19], BTVar[21], BTVar[22], BTVar[23], 1, 0, vehId1)
        cur = conn.cursor()
        cur.execute(sql, queryParam)
'''    


def update_Latest_data_by_VehId(conn, vehId1, date_time,mylist):
    #pass vehId and get the data from Latest_data table 
    # If latest data is none - means data not exists -> Need to insert
    # If latest data is not none - means data exists -> Need to update
    #print mylist

    try:
    
        cur = conn.cursor()
        cur.execute("DELETE FROM Latest_data WHERE vehId=?",(vehId1,))
                
        rows = cur.fetchall()
        #print rows
        #print len(BTVar)

        for i in range(2, len(mylist)):

            position = mylist[i][6]
            print position
            
            if position != '00' and position != '0' :
            
            
                sensorid =  mylist[i][7]+mylist[i][8]+mylist[i][9]
                pres = mylist[i][10]+mylist[i][11]
                temp = mylist[i][12]

                statstr = mylist[i][13]
                statint =  (int(statstr, 16))
                

                presint_Bar = ((int(pres, 16)*0.025))
                presint_Psi =  ((presint_Bar * 14.5038))
                dispPsi = str((presint_Psi))

                tempint_Celcious  = (int(temp, 16) - 50)
                disptemp = (int(tempint_Celcious))

                sql = ''' INSERT INTO Latest_data (vehId,device_date_time,
                                location,
                                sensorId,
                                pressure,
                                temp,
                                sensor_status,
                                status, count)
                                VALUES(?,?,?,?,?,?,?,?,?) '''
                              

                queryParam = (vehId1, date_time, position, sensorid, presint_Psi, tempint_Celcious, statint, 1, 0)
                cur = conn.cursor()
                cur.execute(sql, queryParam)
                
                print "Need to insert", (vehId1, date_time, position, sensorid, presint_Psi, tempint_Celcious, statint)

        conn.commit()

    except sqlite3.Error as e:
        print ("Failed - Accessing to DB table TyreDetails by Vehicle ID - Not Available: ",VehId1)
        my_logger.error("Failed - sqlite3.Error and Accessing to DB table TyreDetails by Vehicle ID - Not Available: %d, %d ",e, VehId1)
        #raise
        #conn.close()
        return None

    
                

#update_task(conn, (2, '2015-01-04', '2015-01-06',2))

def main():
    
    database = "/opt/Aquire/sqlite/TPMS.db"
    print (" DB Create a connection ")
    
    #create a connection to database
    conn = create_db_connection(database)
    #time.sleep(0.5)
    #conn.close()

    #BluetoothSocketVariable = ('01', 'ba6b09', '000000', '00', '02', 'ba6d6d', '000000', '00', '03', '56a8cb', '000000', '00', '04', '56a6be', '000000', '00', '05', '56a781', '000000', '00', '06', '56a7c5', '000000', '00')
    #tag = "e2000016351702081640767faa"
    tag = None
    vehID = 1

    rows = 8
    columns= 16
    mylist = [['0' for x in range(columns)] for x in range(rows)]

    mylist = [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], \
              [0, 'a1', '41', '08', '63', '00', '06'], \
              [0, 'a1', '41', '0f', '63', '00', '01', 'ba', '6b', '09', '01', '18', '70', '00'], \
              [0, 'a1', '41', '0f', '63', '00', '02', 'ba', '6d', '6d', '01', '10', '00', '00'], \
              [0, 'a1', '41', '0f', '63', '00', '03', '56', 'a8', 'cb', '01', '10', '80', '00'], \
              [0, 'a1', '41', '0f', '63', '00', '04', '56', 'a6', 'be', '01', '10', '00', '00'], \
              [0, 'a1', '41', '0f', '63', '00', '05', '56', 'a7', '81', '01', '10', '00', '00'], \
              [0, 'a1', '41', '0f', '63', '00', '06', '56', 'a7', 'c5', '01', '10', '00', '00']]


    
    
    #print conn
    with conn:
        #select_DeviceDetails_by_rfiduid(conn, tag)
        #select_TyreDetails_by_VehId(conn, vehID)
        #conn.close()

        
        status = update_Latest_data_by_VehId(conn, vehID, mylist)
        print "Connecton Close", status, conn

        
    conn.close()

if __name__ == '__main__':

    
    main()
