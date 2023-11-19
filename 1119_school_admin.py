import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

conn = st.connection("gsheets", type=GSheetsConnection)
existing_data = conn.read(worksheet='trial_account', usecols=list(range(10)))

existing_data = existing_data.dropna(how="all")

st.dataframe(existing_data)
