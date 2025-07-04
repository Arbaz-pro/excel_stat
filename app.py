import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os

st.set_page_config(page_title="Excel Data Statistical Analyzer", layout="wide")
if "page" not in st.session_state:
    st.session_state.page = "upload"
# Go back button
if st.session_state.page == "analyze":
    if st.button("Go Back"):
        st.session_state.page = "upload"
        st.session_state.df = None

if st.session_state.page == "upload":
    st.title("Upload Excel or CSV File")
    uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["csv", "xlsx"])
    if uploaded_file:
        file_ext = os.path.splitext(uploaded_file.name)[1]
        if file_ext == ".csv":
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        else:
            df = pd.read_excel(uploaded_file)
        df.rename(columns={
        df.columns[20]: "Leak Type",
        "Plant Name": "Plant",
        "SO": "State Office"
    }, inplace=True)
        
        st.session_state.df = df
        st.session_state.page = "analyze"
        st.rerun()
elif st.session_state.page == "analyze":
    df = st.session_state.df
    ndf=df[["State Office","Plant","Distributor Code","Distributor Name","Territory","Leak Type",]]
    fil_df=ndf.copy()

#add dropdowns to filter data
    col1, col2, col3 = st.columns(3)
    with col1: 
        state_options =["ALL"] + sorted(ndf["State Office"].dropna().unique())
        sel_state = st.multiselect("State Office",state_options)
    fil_df = ndf.copy()
    if sel_state==[]:
         fil_df=fil_df[fil_df["State Office"].isin(state_options)]
    else:
        fil_df=fil_df[fil_df["State Office"].isin(sel_state)]
        with col2:
            sel_plant = st.multiselect("Plant", sorted(fil_df["Plant"].dropna().unique()))
            if sel_plant:
               fil_df=fil_df[fil_df["Plant"].isin(sel_plant)]
        
    with col3:
        sel_leak = st.multiselect("Leak Type", sorted(fil_df["Leak Type"].dropna().unique()))
        if sel_leak:
            fil_df = fil_df[fil_df["Leak Type"].isin(sel_leak)]  
            
# add tabs to distribute data
          
    tab1,tab2,tab3=st.tabs(["Charts","Filter data","Group by"])

# first tab for charts
    
    with tab1:
        if "ALL" in sel_state:
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
        else :  
            if sel_plant:
                st.subheader("Leak–wise Total Complaints")
                leak_c=fil_df["Leak Type"].value_counts().reset_index()
                leak_c.columns = ["Leak Type", "Total Complaints"]
                                
                bar_fig = px.bar(
                leak_c,
                x="Leak Type",
                y="Total Complaints",
                title="Total Complaints by Leak Type",
                text="Total Complaints",
                color="Total Complaints",
                color_continuous_scale="blues"
                )
                bar_fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(bar_fig, use_container_width=True)

                grouped = (
                fil_df.groupby(["Distributor Name", "Leak Type"])
                .size()
                .reset_index(name="Total Complaints")
                )
                top_dists = (
                grouped.groupby("Distributor Name")["Total Complaints"]
                .sum()
                .nlargest(15)
                .index
                )
                grouped = grouped[grouped["Distributor Name"].isin(top_dists)]
                color_palette = ["#1f77b4", "#4c72b0", "#6baed6", "#9ecae1", "#b2df8a", "#a6cee3", "#fdbf6f", "#c7e9c0", "#fb9a99", "#d9d9d9"]
                bar_fig = px.bar(
                grouped,
                x="Distributor Name",
                y="Total Complaints",
                color="Leak Type",
                title="Top 15 Distributors by Complaints, Split by Leak Type",
                text_auto=True,
                color_discrete_sequence=color_palette
                )
                bar_fig.update_layout(xaxis_tickangle=-45,barmode="stack")
                st.plotly_chart(bar_fig, use_container_width=True)
            else:
                st.subheader("Plant–wise Total Complaints")
                plant_count=fil_df["Plant"].value_counts().reset_index()
                plant_count.columns = ["Plant", "Total Complaints"]
                                
                bar_fig = px.bar(
                plant_count,
                x="Plant",
                y="Total Complaints",
                title="Total Complaints by Plant",
                text="Total Complaints",
                color="Total Complaints",
                color_continuous_scale="blues"
                )
                bar_fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(bar_fig, use_container_width=True) 

                dist_count=fil_df["Distributor Name"].value_counts().reset_index()
                dist_count.columns = ["Distributor Name", "Total Complaints"]
                
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
        
        
        
    with tab2:
        st.dataframe(fil_df)
        
        
    with tab3:
        group_cols = [
        "State Office", 
        "Plant", 
        "Distributor Name", 
        "Leak Type"
    ]

        if all(col in fil_df.columns for col in group_cols):
            grouped_df = (
                fil_df.groupby(group_cols)["Leak Type"].size().reset_index(name="Count"))

            st.subheader("Grouped Complaint Summary")
            st.write(grouped_df)
