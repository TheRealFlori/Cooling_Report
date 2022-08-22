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
    mycol = mydb["Cooling Reporting"]

    # get all data from collection
    data = mycol.find({})
    # convert to pandas dataframe
    df = pd.DataFrame(data)
    # print data
    print(df)

except Exception as e:
    st.write(e)

col1, col2 = st.columns(2)
col1.metric("Aktuelle Temperatur Kühlschrank", "10 °C", "1.2 °C")
col2.metric("Aktuelle Temperatur Gefrierschrank", "- 10 °C", "1.2 °C")

col1, col2 = st.columns(2)
col1.metric("Durchschnittstemperatur der letzten 24 h im Kühlschrank", "10 °C", "1.2 °C")
col2.metric("Durchschnittstemperatur der letzten 24 h im Gefrierschrank", "- 10 °C", "1.2 °C")

chart_data = pd.DataFrame(
    np.random.randn(20, 2),
    columns=['Temperatur Kühlschrank', 'Temperatur Gefrierschrank'])

st.line_chart(chart_data)
