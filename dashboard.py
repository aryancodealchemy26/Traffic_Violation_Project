import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Traffic Violation Dashboard", layout="wide")

st.title("🚦 Traffic Violation Detection System")
st.write("Dashboard loaded successfully ✅")

if os.path.exists("violations.csv"):
    df = pd.read_csv("violations.csv")

    st.write("CSV file found ✔️")
    st.write("Total records:", len(df))

    st.dataframe(df, use_container_width=True)

    st.subheader("Severity Distribution")
    st.bar_chart(df["Severity"].value_counts())
else:
    st.error("violations.csv not found ❌")
