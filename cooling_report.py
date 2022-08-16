from ipaddress import collapse_addresses
import streamlit as st # pip install stremlit
import pymongo # pip install pymongo
import pandas as pd
import numpy as np

import calendar
import datetime

#--------------------------- SETTINGS ------------------
page_title = "BRK Regenstauf Temperatur Überwachung"
page_icon = "Bereitschaftslogo.jpg"
layout = "centered"
#-------------------------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title)

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

try:
    client = init_connection()
    check = client.jack
    ServerStat = check.command("serverStatus")
    st.write(ServerStat)
    st.write("Mongo Database sucessfully connected")

except Exception as e:
    st.write(e)

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

# Pull the collection.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def get_data():
    db = client['brk-regenstauf']
    col = db['Cooling Reporting']
    return col

items = get_data()
count = items.count_documents({})

# Print results.
st.write(count)
