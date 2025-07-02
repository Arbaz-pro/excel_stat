import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Excel Data Statistical Analyzer", layout="wide")

st.title(" Excel Data Statistical Analyzer")

uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
    df.rename(columns={
    df.columns[20]: "Leak Type",
    "Plant Name": "Plant",
    "SO": "State Office"
}, inplace=True)
    ndf=df[["Distributor Name","Distributor Code","Plant","Territory","Leak Type","State Office"]]
    st.write("columns",ndf.columns)
    st.sidebar.header("Filter")
    sel_state=st.sidebar.multiselect("State Office",ndf["State Office"].dropna().unique())
    fil_df=ndf.copy()
    if sel_state:
        fil_df=fil_df[fil_df["State Office"].isin(sel_state)]
        sel_plant=st.sidebar.multiselect("Plant",fil_df["Plant"].dropna().unique())
        if sel_plant:
           fil_df=fil_df[fil_df["Plant"].isin(sel_plant)] 
        st.write("Selected Plants:", sel_plant if 'sel_plant' in locals() else [])
    st.write("State",sel_state)
else:

    st.info("Please upload a file to start analysis.")
