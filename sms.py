#file to read sms on a linux environment like raspberry running on raspbian
import sys
import time
import gammu
import requests
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#firebase authentication
cred = credentials.Certificate("path/to/file.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://xxx.firebaseio.com/'
})

try:
    #reading sms configs
    sm = gammu.StateMachine()
    sm.ReadConfig()
    sm.Init()
except Exception as e:
    #logging sms errors. I later on discoverd the loggin library
    with open("readsmserrors", "a") as file:
        file.write(time.ctime()+" Fatal Error in SMS Configs. Has the modem been detected? "+str(e)+" Exiting Script\n")
    sys.exit()  
  
while True:
    try:
        #checking for any unread sms
        status = sm.GetSMSStatus()
        remain = status['SIMUsed'] + status['PhoneUsed'] + status['TemplatesUsed']
        start = True

        while remain > 0:
            if start:
                #reading unread sms
                sms = sm.GetNextSMS(Start = True, Folder = 0)
                start = False
            else:
                sms = sm.GetNextSMS(Location = sms[0]['Location'], Folder = 0)
            remain = remain - len(sms)

            for m in sms:
                #senfing data to firebase
                text = [x.strip() for x in m['Text'].split(',')]
                firebase = db.reference('/'+str(text[0])+'/data')
                firebase.update({"id":text[1], "time":text[2]})
		#saving the data locally to be sent later to a remote database
                with open("getdata", "a") as file:
                    file.write(m['Text']+"\n")
                
                #deleting the sms after reading
                sm.DeleteSMS(m['Folder'], m['Location'])
    except Exception as e:
        with open("readsmserrors", "a") as file:
            file.write(time.ctime()+" Error in SMS Main Thread. Has the modem been detected? "+str(e)+" \n")
            
