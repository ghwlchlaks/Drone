#!/usr/bin/env python
#coding=utf-8

##########################################################################################
from datetime import datetime, timedelta
import pprint
from influxdb import InfluxDBClient
from copy import deepcopy
import pytz
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("--data",help="sensor data input")
args=parser.parse_args()
sensor_data = args.data
print(sensor_data)

sensor_Id = sensor_data.split(',')[0]
temperature_data = sensor_data.split(',')[1]
humidity_data = sensor_data.split(',')[2]
illu_data = sensor_data.split(',')[3]
measured_time = sensor_data.split(',')[4]

##########################################################################################
local_tz = pytz.timezone('Asia/Seoul') # use your local timezone name here
##########################################################################################
def utc_to_local(utc_dt):
	local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
	return local_tz.normalize(local_dt) # .normalize might be unnecessary

##########################################################################################
def get_ifdb(db, host='localhost', port=8086, user='root', passwd='root'):
	client = InfluxDBClient(host, port, user, passwd, db)
	try:
		client.create_database(db)
	except:
		pass
	return client

##########################################################################################
def my_test(ifdb):
	json_body = [
	]
	tablename = 'Drone1'
	fieldname1 = 'sensor_ID'
	fieldname2 = 'temperature'
	fieldname3 = 'humidity'
	fieldname4 = 'illu'
	fieldname5 = 'measured time'
	
	point = {
		"measurement": tablename,
		"tags": {
			"host": "Anyang",
			"team": "NeeDroN"
		},
		"fields": {
			fieldname1: 0,
			fieldname2: 0,
			fieldname3: 0,
			fieldname4: 0,
			fieldname5: None 
		},
		"time": None,
	}
	dt = datetime.now()
	ldt = utc_to_local(dt)
	print "UTC now=<%s> local now=<%s>" % (dt, ldt)
	global sensor_Id , temperature_data , humidity_data , illuminate_data , measured_time
	np=deepcopy(point)
	np['fields'][fieldname1] = int(sensor_Id)
	np['fields'][fieldname2] = float(temperature_data)
	np['fields'][fieldname3] = float(humidity_data)
	np['fields'][fieldname4] = float(illu_data)
	np['fields'][fieldname5] = measured_time
	np['time'] = dt
	json_body.append(np)
	ifdb.write_points(json_body)


##########################################################################################
def do_test():
	ifdb = get_ifdb(db='NeeDroN')
	my_test(ifdb)

##########################################################################################
if __name__ == '__main__':
	do_test()
