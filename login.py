#this file logins a raspberry device to a remote server to allow it send data to the API
import time
import requests
import os
import base64
import json
from datetime import datetime,timedelta

filename = "/my/path/to/file.txt"

def login(logins):
    """login function"""
    API_ENDPOINT = "xxx.xxx.xxx.xxx:8000/login"
    headers={"Content-Type": "application/json"}
    logins = json.dumps(logins)
    response = requests.post(API_ENDPOINT,headers=headers,data = logins)
    json_response = response.json()
    return json_response

def read_logins():
    """reads login details from file"""
    with open(filename, "r") as read_file:
        try:
            datas = json.load(read_file)
            logins = {
                "userEmail":datas["deviceUID"],
                "userPassword":base64.b64decode(datas["devicePassword"]).decode('utf-8'),
                "userType":datas["deviceUsername"]
            }
        except:
            print("Unable to fetch configs.")
            os.exit()
    return logins

def accessToken():
    """fatches access token"""
    try:
        logins = read_logins()
        resp = login(logins)
        token = resp['accessToken']
        expiresAt = resp['expiresAt']
        expiresAt = datetime.strptime(expiresAt, '%Y-%m-%dT%H:%M:%S.%f')
    except:
        return False
    return token, expiresAt
    