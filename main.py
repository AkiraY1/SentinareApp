import requests, time

id = "tssOCgWHeoFCF6ym"
secret = "IWI7gfUGRmYvJy83VXZhnik0Dsy6HinMC6GQ2bpawZR7te6GLW8IvBEDsiJPAFZ1"
access_token = "aa475216f6aae2b0ec911e75d2d28e4d7579ada1"
#Expires in 60 days

base = "https://api.altumview.ca/v1.0/"
baseOAuth = "https://canada-1.oauth.altumview.com/v1.0/token"

def getAccessToken():
    params = {"grant_type": "client_credentials", "client_id": id, "client_secret": secret, "scope": "room:write room:read camera:write camera:read alert:read alert:write person:write person:read"} #Gets client credentials
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(baseOAuth, data=params, headers=headers)
    return response.json()["access_token"]

def getVisits():
    url = "https://api.altumview.ca/v1.0/visits"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    return response.text

print(getAccessToken())