import requests

id = "BQt1NqlxO8LIYUeQ"
secret = "bpoUuwxWmwvcZXI9i3PSSDtvSA6OMGjere1PsR1vUSyCOn0ZE6cjkFA4rAz9EvbD"
access_token = "838ac2880e417a0cd210a268a3a3c8922ee7d4e1"
#Expires in 60 days (Thursday, April 14, 2022)

base = "https://api.altumview.ca/v1.0/"
baseOAuth = "https://canada-1.oauth.altumview.com/v1.0/token"

def getAccessToken():
    params = {"grant_type": "client_credentials", "client_id": id, "client_secret": secret,
        "scope": "room:write room:read camera:write camera:read"} #Gets client credentials
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(baseOAuth, data=params, headers=headers)
    return response.content

def getRooms():
    url = base+"rooms"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    return response.content

def getUserInfo():
    url = base+"info"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    return response.content