###############################################################
# TMS RFID Serial Integration -09-2017
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

#Serial Enable
serial = serial.Serial("/dev/ttyS0", baudrate = 9600, timeout = 0.2)

#Variable Decleration
s = 'hello'
data = []
rfidTID_hex = []
rfidTID = []
cksm = []

TID1 = "e2000016351702081640767f"

#RFID Query Tag
def RFIDUHFQueryTag(): 

    QueryTag = "040001DB4B"

    my_hex = QueryTag.decode('hex')
    #print my_hex        
    print binascii.b2a_hex(my_hex)
    serial.write(my_hex)
    #serial.write("Hello World")

    #print " ".join(hex(ord(n)) for n in my_hex)

#Read RFID data and Check
#def ParseRFIDResponse():
    
    data = serial.readline()
    #print data
    
    if(data[3] == '\x01'):
       
        
        #rfid = binascii.b2a_hex(data)
        rfidTID_hex = binascii.b2a_hex(data)
        #print rfidTID_hex
        rfidTID = rfidTID_hex [12:36]
        #RFID TAG ID Data
        print rfidTID

        if rfidTID == TID1:
            print "Hello"

    return rfidTID

if __name__ == "__main__":  
    
    RFIDUHFQueryTag()
