import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Excel Data Statistical Analyzer", layout="wide")

st.title(" Excel Data Statistical Analyzer")

uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["csv", "xlsx"])

if uploaded_file.name.endswith('.csv'):
    df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
    df.rename(columns={
    "Mechanic ‘s response on leakage type": "Leak Type",
    "Plant Name": "Plant",
    "SO": "State Office"
}, inplace=True)
    st.write("columns",df.columns[-2])
    
else:
    st.info("Please upload a file to start analysis.")
