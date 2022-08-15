from ipaddress import collapse_addresses
import streamlit as st # pip install stremlit
import pymongo # pip install pymongo

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
    st.write("Mongo Database sucessfully connected")

except Exception as e:
    st.write(e)

# Pull data from the collection.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def get_data():
    db = client["brk-regenstauf"]
    col = db["Cooling Reporting"].find()
    col = list(col)
    return col

items = get_data()

# Print results.
st.write(items)
