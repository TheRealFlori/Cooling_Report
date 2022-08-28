from ipaddress import collapse_addresses
import streamlit as st  # pip install .streamlit
import pymongo  # pip install pymongo
import pandas as pd
import numpy as np

import calendar
import datetime

# --------------------------- SETTINGS ------------------
page_title = "BRK-Regenstauf Temperatur Überwachung"
page_icon = "Bereitschaftslogo.jpg"
layout = "centered"
# -------------------------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title)


# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    print("Initializing connection...")
    return pymongo.MongoClient((st.secrets["url"]).conn)


try:
    # get Client
    client = init_connection()
    # connect to DB
    mydb = client["brk-regenstauf"]
    # get collection
    mycol = mydb["coolingreporting"]

    # get all data from collection
    freezer = mycol.find({"type": "freezer"})
    fridge = mycol.find({"type": "fridge"})
    col = mycol.find({})
    # convert to pandas dataframe
    p_freezer = pd.DataFrame(freezer)
    p_fridge = pd.DataFrame(fridge)
    df = pd.DataFrame(col)
    # print data
    print("freezer")
    print(p_freezer)
    print("fridge")
    print(p_fridge)

except Exception as e:
    st.write(e)

st.subheader("Aktuelle Temperatur")
col1, col2 = st.columns(2)
col1.metric("Aktuelle Temperatur Kühlschrank", p_fridge.get("temperature").iloc[-1:], "1.2 °C")
col2.metric("Aktuelle Temperatur Gefrierschrank", p_freezer.get("temperature").iloc[-1:], "1.2 °C")

st.subheader("Durchschnittliche Temperatur der letzten 24 Stunden")
col1, col2 = st.columns(2)
col1.metric("Durchschnittstemperatur im Kühlschrank", p_fridge["temperature"].mean(), "1.2 °C")
col2.metric("Durchschnittstemperatur im Gefrierschrank", p_freezer["temperature"].mean(), "1.2 °C")

st.subheader("Test")
col1, col2 = st.columns(2)
col1.write("Freezer")
col1.write(p_freezer.get(["time", "temperature"]))

col2.write("Fridge")
col2.write(p_fridge.get(["time", "temperature"]))

st.line_chart(df.get(["time", "temperature"]))

chart_data = pd.DataFrame(
    df.get("time"),
    df.get("temperature"),
    columns=df.get("type"))

st.line_chart(chart_data)

st.line_chart(data=none, x=df.get("time"), y=df.get("temperature"))

#for seconds in range(200):
#xxx
#time.sleet(1)
