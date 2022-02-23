import requests, time, datetime, threading
import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

id = "tssOCgWHeoFCF6ym"
secret = "IWI7gfUGRmYvJy83VXZhnik0Dsy6HinMC6GQ2bpawZR7te6GLW8IvBEDsiJPAFZ1"
access_token = "aa475216f6aae2b0ec911e75d2d28e4d7579ada1"
base = "https://api.altumview.ca/v1.0/"
baseOAuth = "https://canada-1.oauth.altumview.com/v1.0/token"

BUFF = 1800 #30 minutes

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

visits = {}
def logVisits():
    for visit in getVisits():
        dep_time = visit["departure_time"]
        id = visit["person"]["id"] #Gets ID instead of name in case multiple people have the same name
        if id in visits:
            visits[id].append(dep_time)
        else:
            visits[id] = [dep_time]
    print(visits)

def makeGraph(fro, to):
    df = pd.DataFrame({ 'from':fro, 'to':to})
    G = nx.from_pandas_edgelist(df, 'from', 'to')
    nx.draw(G, with_labels=True, node_size=1500, node_color="skyblue", pos=nx.fruchterman_reingold_layout(G))
    st.pyplot(plt)

def in_list(val, val_list):
    items = []
    for item in val_list:
        if (item > val-BUFF) and (item < val+BUFF) and (item != val):
            items.append(item)
    return items

def makeNetwork():
    global visits
    global date
    to = []
    fro = []
    if len(visits) > 1:
        val_list = []
        for val in visits.values():
            for vis in val:
                val_list.append(vis)
        for val in val_list:
            corresponding_values = in_list(val, val_list) #-1 for none or returns index, use index to find id, use id to connect IDs in to-fro list
            if corresponding_values != []:
                #Find id of corresponding value
                ### Use [(i, colour.index(c)) for i, colour in enumerate(colours) if c in colour] to find index

    else:
        st.warning(f"There is only 1 person who has been detected since {date}.")
        makeGraph([1], [1])

st.set_page_config(page_title="Sentinare Contact Tracing",)
st.title("Sentinare Disease Contact Tracing")
user_id = st.sidebar.text_input('API Credential ID')
user_secret = st.sidebar.text_input('API Secret')
date = st.sidebar.date_input("Search from...", datetime.date.today())
submit = st.sidebar.button('Submit')
if submit:
    if user_id and user_secret and date:
        #if details check out --------------------------------------------------------
        logVisits()
        with st.spinner('Loading...'):
            time.sleep(2)
        fig = makeNetwork()
        st.sidebar.success("Success!")
    else:
        st.sidebar.error("Fill all fields.")



#Need to put entrance and exit
#Can't restrict time in both directions
#Hard to see face