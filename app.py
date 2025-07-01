import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Excel Data Statistical Analyzer", layout="wide")

st.title(" Excel Data Statistical Analyzer")

uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["csv", "xlsx"])

if uploaded_file.name.endswith('.csv'):
    try:
        df = pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        # Try fallback encoding if UTF-8 fails
        df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        st.stop()
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df.head())
    st.subheader("complaint count state office wise")
    so_column = df.columns[-1] 
    so_counts = df[so_column].dropna().value_counts().reset_index()
    so_counts.columns = ['State Office', 'Total Count']
    fig = px.bar(so_counts, x='State Office', y='Total Count', title='Count per State Office', text='Total Count')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    leak_column = df.columns[-3]  
    leak_counts = df[leak_column].dropna().value_counts().reset_index()
    leak_counts.columns = ['leak', 'Total Count']
    figs = px.bar(leak_counts, x='leak', y='Total Count', title='Count per leak', text='Total Count')
    figs.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(figs, use_container_width=True)

    st.subheader("🎛️ Filter by State Office, Plant, and Leak Type")

    # Replace these with actual column names from your dataset
    so_col = df.columns[-1]             # State Office (e.g., 'Gujarat SO-LPG')
    plant_col = df.columns[2]           # Plant (e.g., 'Patna BP-IOC')
    leak_col = 'ing'                    # Leak Type column (based on your screenshot)
    
    # Dropdown filters
    selected_so = st.selectbox("Select State Office", options=['All'] + sorted(df[so_col].dropna().unique().tolist()))
    selected_plant = st.selectbox("Select Plant", options=['All'] + sorted(df[plant_col].dropna().unique().tolist()))
    selected_leak = st.selectbox("Select Leak Type", options=['All'] + sorted(df[leak_col].dropna().unique().tolist()))

    st.dataframe(df[plant_col])
    
else:
    st.info("Please upload a file to start analysis.")
