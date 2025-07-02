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
    df.rename(cloumns={"Mechanic ‘s response on leakage type"
:"Leak Type","Plant Name":,"Plant","SO":"State Office"}.inplace=True)

    st.subheader("Data Preview")
    st.dataframe(df.head(15))
    
else:
    st.info("Please upload a file to start analysis.")
