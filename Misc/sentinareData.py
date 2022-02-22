from getpass import getuser
from os import access
import requests, time

id = "tssOCgWHeoFCF6ym"
secret = "IWI7gfUGRmYvJy83VXZhnik0Dsy6HinMC6GQ2bpawZR7te6GLW8IvBEDsiJPAFZ1"
access_token = "76b082ec165bdeae5ca51ad3ac255881097eabe7"
#Expires in 60 days

base = "https://api.altumview.ca/v1.0/"
baseOAuth = "https://canada-1.oauth.altumview.com/v1.0/token"

def getAccessToken():
    params = {"grant_type": "client_credentials", "client_id": id, "client_secret": secret, "scope": "room:write room:read camera:write camera:read alert:read alert:write person:write person:read"} #Gets client credentials
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(baseOAuth, data=params, headers=headers)
    return response.content

def getRooms():
    url = base+"rooms"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    return response.content

def getUserInfo():
    url = "https://api.altumview.ca/v1.0/info"
    auth = "Bearer " + access_token
    headers = {"Authorization": auth}
    response = requests.get(url, headers=headers)
    return response.text

def getMQTTAccount():
    url = base+"mqttAccount"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    return response.content

def getAlerts():
    #Anything that happened in the past hour (check every hour)
    url = base+"alerts"
    headers = {"Authorization": "Bearer " + access_token}
    start_date = time.time() - 3600
    end_date = time.time() - 1000
    params = {"start_date": start_date, "end_date": end_date}
    response = requests.get(url, headers=headers)
    return response.content

def getBackground():
    url = "https://api.altumview.ca/v1.0/cameras/885/background" #Make id variable later
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    return response.content

def getCameras():
    url = "https://api.altumview.ca/v1.0/cameras"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    return response.content

def streamToken():
    url = "https://api.altumview.ca/v1.0/cameras/887/streamtoken"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    return response.content

def getAlertbyID(id):
    url = f"https://api.altumview.ca/v1.0/alerts/{id}"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    return response.headers

def getView(id):
    url = f"https://api.altumview.ca/v1.0/cameras/{id}/view/"
    print(url)
    headers = {"Authorization": "Bearer " + access_token}
    params = {"preview_token": "1857017006"}
    response = requests.get(url, params=params, headers=headers)
    return response.text

def getBluetoothToken():
    url = f"https://api.altumview.ca/v1.0/cameras/bluetoothToken?serial_number=237DA6E9452898EE"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    return response.text

def getCalibratedFloor():
    url = "https://api.altumview.ca/v1.0/cameras/887/floormask"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    return response.text

def getVisits():
    url = "https://api.altumview.ca/v1.0/visits"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    return response.text

print(getVisits())