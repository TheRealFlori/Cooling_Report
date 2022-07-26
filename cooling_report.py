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

client = pymongo.MongoClient("mongodb+srv://brk-regenstauf-read:aBxpdD9AVsEAnvUk@brk-regenstauf.iw6ulrw.mongodb.net/?retryWrites=true&w=majority")
db = client["brk-regenstauf"]
