#!/usr/bin/env python

from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
from pymavlink import mavutil



#connection_string ="/dev/ttyACM0"
connection_string ="udp:127.0.0.1:14550"

# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % connection_string
vehicle = connect(connection_string, wait_ready=True)
vehicle.parameters['RTL_ALT']=0  #set RTL mode Altitude 
vehicle.parameters['LAND_SPEED']=30
vehicle.airspeed = 2  #set vehicle speed 

home_location =vehicle.location.global_frame
lat = str(home_location.lat)
lon = str(home_location.lon)
alt = str(home_location.alt)
print(lat+" "+lon+" "+alt)

vehicle.close()

