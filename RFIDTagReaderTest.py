#! /usr/bin/python
#-*-coding: utf-8 -*-

"""
Simple test script for TagReader
Reads a few tags and prints them
Last Modified:
2018/03/07 by Jamie Boyd - added some comments, cleaned up a bit
"""

from RFIDTagReader import TagReader
from datetime import datetime
import os

"""
Change serialPort to wherever your tagreader is
and kind to 'ID' for ID-L3,12,20 etc. or RDM for RDM630 etc.
"""
RFID_serialPort = '/dev/ttyUSB0'
#RFID_serialPort = '/dev/serial0'
#RFID_serialPort='/dev/cu.usbserial-AL00ES9A'
RFID_kind = 'ID'
"""
Setting to timeout to None means we don't return till we have a tag.
If a timeout is set and no tag is found, 0 is returned.
"""
RFID_timeout = None
RFID_doCheckSum = True
read = True

try:
    tagReader = TagReader (RFID_serialPort, RFID_doCheckSum, timeOutSecs = RFID_timeout, kind=RFID_kind)
except Exception as e:
    raise e
i =0

while read:
    try:
        print ('Waiting for tags...')
        tag = tagReader.readTag ()
        print (tag)
        weight_float = input("Please enter the mouse's weight (g): ")
        record_filename = "Mice/"+str(tag)+".csv"

        tm = datetime.now()
        timestamp = str(tm.year) + format(tm.month, '02d') + format(tm.day, '02d') + \
                           format(tm.hour, '02d') + format(tm.minute, '02d') + format(tm.second, '02d')
        i += 1
        summary_exists = os.path.isfile(record_filename)
        if not os.path.exists("Mice/"):
                print("Creating data directory: %s","Mice/")
                os.makedirs("Mice/")

        with open(record_filename, "a") as file:
            if not summary_exists:
                file.write("Timestamp, Tag, Weight\n")
            file.write(timestamp+","+str(tag)+","+str(weight_float)+"\n")


    except ValueError as e:
        print (str (e))
        tagReader.clearBuffer()
print ('Read ' + str (i) + ' tags')
