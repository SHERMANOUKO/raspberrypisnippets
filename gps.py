#function to send gps data from raspberry pi
import serial
import pynmea2
import json
import datetime
import time
import sys
from urllib.request import urlopen
from firebase import firebase

#sets up firebase where data will be sent
firebase = firebase.FirebaseApplication('https://xxxxx-xxx.firebaseio.com/', None)
serialPort = serial.Serial("/dev/ttyS0", 9600, timeout=1)
json_data = {}

#FUnction to parse gps NMEA Strings
def parseGPS(data):
	data = data.decode("utf-8")
	global count
	if data.find('VTG') > 0:
		msg = pynmea2.parse(data)
		json_data['speedKph'] = msg.spd_over_grnd_kmph

	if data.find('RMC') > 0:
		msg = pynmea2.parse(data)
		json_data['speedKnots'] = msg.spd_over_grnd

	if data.find('GGA') > 0:
		msg = pynmea2.parse(data)
		json_data['lat']=float(msg.latitude)
		json_data['lon']=float(msg.longitude)
		json_data['time']=datetime.datetime.now()
		json_data['altitude']=float(msg.altitude)
		json_data['quality']=int(msg.gps_qual)
		json_data['satellites']=int(msg.num_sats)

        if not (storeFirebase(json_data['lat'],json_data['lon'],json_data['time'],json_data['speedKph'])):
            with open('gpsLogs.txt', 'a') as a_writer:
                a_writer.write('\nUnable to save to firebase......'+str(datetime.datetime.now()))
		
		json.dumps(json_data, cls=Encoder, indent=4, sort_keys=True)

#Function to store data to firebase web app section
def storeFirebaseWeb(latitude,longitude,time,speed):
	try:
		storeUrl = '/my/firebase/path/'
		firebase.put(storeUrl,'gpsdata',{'latitude':latitude,'longitude':longitude,'time':time,'speed':str(speed)})
		return True
	except:
		return False

#Function to serialize data
class Encoder(json.JSONEncoder):
	def default(self, obj):
		try:
			if isinstance(obj, datetime.datetime):
				return obj.isoformat()
			else:
                        	return json.JSONEncoder.default(self, obj)
		except:
			with open('gpsLogs.txt', 'a') as a_writer:
				a_writer.write('\nUnable to encode data during serialization......'+str(datetime.datetime.now()))

while True:
	try:
		data = serialPort.readline()
		parseGPS(data)
		time.sleep(0.25)
	except:
		pass

