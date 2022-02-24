from re import L
import requests, time, datetime, threading
import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sentinare Contact Tracing", page_icon="🟦", initial_sidebar_state="expanded")
st.title("Sentinare Infection Contact Tracing")
with st.expander("See Instructions"):
     st.write("""
         Welcome to AltumView's infections contact tracing platform for the Sentinare! 
         This web app allows you to view possible/likely connections between individuals in a senior home in order to trace who might have been exposed to an infection (e.g. COVID-19).
         \nIn order to use this service:
            \n1. Mark the entire view of your Sentinare camera(s) as a region of interest (ROI) of type "Exit" (we only begin tracking visits for contact tracing AFTER marking the ROI, so make sure to do this LONG before using this web app).
            \n2. Enter your API credential ID and secret on the left.
            \n3. Enter your desired "time interval"; the maximum difference of time when two or more people entered the room but could still infect each other. For example, this could be set to the length of time COVID-19 viruses can live on a surface or in the air.
            \n4. Enter how far back you wish to contact trace. For example, this might be 2 weeks if an individual under your care just tested positive for COVID-19, since the incubation period can be up to two weeks.
            \n5. Submit! The resulting network graph will show all connections between invididuals who might have infected each other. The table below provides details for the times at which each person could have been infected.
     """)

access_token = ""
BUFF = 7200 #In seconds (2 hours by default)

def getAccessToken(id, secret):
    url = "https://canada-1.oauth.altumview.com/v1.0/token"
    params = {"grant_type": "client_credentials", "client_id": id, "client_secret": secret, "scope": "room:write room:read camera:write camera:read alert:read alert:write person:write person:read"} #Gets client credentials
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=params, headers=headers)
    return response.json()

def getVisits():
    url = "https://api.altumview.ca/v1.0/visits"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    return response.json()["data"]["visits"]["array"]

def getPerson(id):
    print(id)
    url = f"https://api.altumview.ca/v1.0/people/{id}"
    auth = "Bearer " + access_token
    headers = {"Authorization": auth}
    response = requests.get(url, headers=headers)
    name = response.json()["data"]["person"]["friendly_name"]
    role = response.json()["data"]["person"]["person_group"]["name"]
    return name, role

visits = {}
table = []

def logVisits(d):
    dt = datetime.datetime.combine(d, datetime.datetime.min.time())
    for visit in getVisits():
        dep_time = visit["departure_time"]
        id = visit["person"]["id"] #Gets ID instead of name in case multiple people have the same name
        if dt.timestamp() < dep_time:
            if id in visits:
                visits[id].append(dep_time)
            else:
                visits[id] = [dep_time]

def makeGraph(fro, to):
    df = pd.DataFrame({ 'from':fro, 'to':to})
    G = nx.from_pandas_edgelist(df, 'from', 'to')
    nx.draw(G, with_labels=True, node_size=1500, node_color="#648cd4", pos=nx.fruchterman_reingold_layout(G))
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
    global table
    fro = []
    to = []
    h = list(visits.values())
    c = list(visits.keys())
    print(h)
    if len(visits) > 1:
        val_list = []
        for val in h:
            for vis in val:
                val_list.append(vis)
        for val in val_list:
            index1 = [(i, visitTime.index(val)) for i, visitTime in enumerate(h) if val in visitTime]
            visitor1_id = c[index1[0][0]]
            name1, role1 = getPerson(visitor1_id)
            
            new_row = [datetime.datetime.fromtimestamp(val), name1, visitor1_id, role1]
            table.append(new_row)

            corresponding_values = in_list(val, val_list) #-1 for none or returns index, use index to find id, use id to connect IDs in to-fro list
            if corresponding_values != []:
                for cor_val in corresponding_values:
                    index2 = [(i, visitTime.index(cor_val)) for i, visitTime in enumerate(h) if cor_val in visitTime]
                    visitor2_id = c[index2[0][0]]

                    name2, role2 = getPerson(visitor2_id)
                    new_row = [datetime.datetime.fromtimestamp(cor_val), name2, visitor2_id, role2]
                    table.append(new_row)
                    
                    fro.append(visitor1_id)
                    to.append(visitor2_id)
        df = pd.DataFrame(table, columns=['Time', 'Name', 'ID', 'Group'])
        makeGraph(fro, to)
        df_adj = df.drop_duplicates(keep="first")
        st.dataframe(df_adj)
    else:
        st.warning(f"There is only 1 person who has been detected since {date}.")
        name, role = getPerson(c[0])
        print(h)
        table.append([datetime.datetime.fromtimestamp(h[0][0]), name, c[0], role])
        df = pd.DataFrame(table, columns=['Time', 'Name', 'ID', 'Group'])
        makeGraph([c[0]], [c[0]])
        df_adj = df.drop_duplicates(keep="first")
        st.dataframe(df_adj)

########################################################################################################################

user_id = st.sidebar.text_input('API Credential ID')
user_secret = st.sidebar.text_input('API Secret')
BUFF = st.sidebar.number_input('Time interval (minutes)', min_value=1, max_value=2628000, value=120, step=1)*60
date = st.sidebar.date_input("Search from...", datetime.date.today())
submit = st.sidebar.button('Submit')
if submit:
    if user_id and user_secret and date and BUFF:
        token = getAccessToken(user_id, user_secret)
        if token["success"]:
            access_token = token["access_token"]
            with st.spinner('Loading...'):
                logVisits(date)
                if visits != {}:
                    makeNetwork()
                    st.sidebar.success("Success!")
                else:
                    st.warning("No visits during time interval selected")
        else:
            st.sidebar.error("Incorrect API ID or secret")
    else:
        st.sidebar.error("Please fill all fields.")

#Problems:
# Need to put entrance and exit
# Can't restrict time in both directions
# Hard to see face