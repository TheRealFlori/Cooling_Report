from ipaddress import collapse_addresses
import streamlit as st  # pip install .streamlit
import pymongo  # pip install pymongo
import pandas as pd
import numpy as np

import calendar
import datetime

from numpy.distutils.fcompiler import none
from streamlit.elements.arrow_altair import _melt_data

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
    pfreezer = pd.DataFrame(freezer)
    pfridge = pd.DataFrame(fridge)
    df = pd.DataFrame(col)
    # print data
    print("freezer")
    print(pfreezer)
    print("fridge")
    print(pfridge)

except Exception as e:
    st.write(e)

st.subheader("Aktuelle Temperatur")
col1, col2 = st.columns(2)
col1.metric("Aktuelle Temperatur Kühlschrank", pfridge.get("temperature").iloc[-1:] , "1.2 °C")
col2.metric("Aktuelle Temperatur Gefrierschrank", pfreezer.get("temperature").iloc[-1:], "1.2 °C")

st.subheader("Durchschnittliche Temperatur der letzten 24 Stunden")
col1, col2 = st.columns(2)
col1.metric("Durchschnittstemperatur im Kühlschrank", round(pfridge["temperature"].mean(),3), "1.2 °C")
col2.metric("Durchschnittstemperatur im Gefrierschrank", round(pfreezer["temperature"].mean(),3), "1.2 °C")

st.subheader("Diagrams")
st.write("Freezer")
# plot "time" and "temperature" of fridge
data = pfridge.get(["time", "temperature"])
st.line_chart(data=data, y="temperature", x="time")

st.write("Fridge")
# plot "time" and "temperature" of freeze
data = pfreezer.get(["time", "temperature"])
st.line_chart(data=data, y="temperature", x="time")
