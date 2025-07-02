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
    
else:
    st.info("Please upload a file to start analysis.")
