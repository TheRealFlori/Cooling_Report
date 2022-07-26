# streamlit_app.py

import streamlit as st
import pymongo

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

try:
    client = init_connection()
    st.write("Mongo connected")

except Exception as e:
    st.write(e)

# Pull data from the collection.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def get_data():
    mydb = client["brk-regenstauf"]
    mycol = mydb["Cooling Reporting"]
    return mycol