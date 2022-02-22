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
    return response.json()["data"]["visits"]["array"]

adj_list = {}

#Schedule to check visits
for visit in getVisits():
    dep_time = visit["departure_time"]
    id = visit["person"]["id"] #Gets ID instead of name in case multiple people have the same name
    if len(adj_list) != 0:
        for person in adj_list:
            for time in person:
                if abs(time[0]-dep_time) < 900: #If time difference between two people is less than 900 seconds (15 mins)
                    adj_list[person].append((id, dep_time))

#Schedule to find links in database