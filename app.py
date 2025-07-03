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
    ndf=df[["State Office","Plant","Distributor Code","Distributor Name","Territory","Leak Type",]]
    st.sidebar.header("Filter")
    set_options=["ALL"] + sorted(ndf["State Office"].dropna().unique())
    sel_state=st.sidebar.multiselect("State Office",set_options,default="ALL")
    fil_df=ndf.copy()
    if "ALL" in sel_state:
        fil_df=fil_df[fil_df["State Office"].isin(set_options)]
    else sel_state:
        fil_df=fil_df[fil_df["State Office"].isin(sel_state)]
        sel_plant=st.sidebar.multiselect("Plant",fil_df["Plant"].dropna().unique())
        if sel_plant:
           fil_df=fil_df[fil_df["Plant"].isin(sel_plant)] 
        sel_leak=st.sidebar.multiselect("Leak Type",fil_df["Leak Type"].dropna().unique(),)
        if sel_leak:
           fil_df=fil_df[fil_df["Leak Type"].isin(sel_leak)] 
      
    tab1,tab2,=st.tabs(["Filter data","Charts"])
    with tab1:
        st.dataframe(fil_df)
    with tab2:
        st.subheader("State Office–wise Total Complaints")
        state_counts = fil_df["State Office"].value_counts().reset_index()
        state_counts.columns = ["State Office", "Total Complaints"]
        
        bar_fig = px.bar(
        state_counts,
        x="State Office",
        y="Total Complaints",
        title="Total Complaints by State Office",
        text="Total Complaints",
        color="Total Complaints",
        color_continuous_scale="blues"
        )
        bar_fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(bar_fig, use_container_width=True)
        
        dist_count=fil_df["Distributor Name"].value_counts().reset_index()
        dist_count.columns = ["Distributor Name", "Total Complaints"]
        st.write("Distributors",dist_count)
        
        bar_fig = px.bar(
        dist_count[:15],
        x="Distributor Name",
        y="Total Complaints",
        title="Top 15 Complaints by Distributors",
        text="Total Complaints",
        color="Total Complaints",
        color_continuous_scale="blues"
        )
        bar_fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(bar_fig, use_container_width=True)
else:
    st.info("Please upload a file to start analysis.")
