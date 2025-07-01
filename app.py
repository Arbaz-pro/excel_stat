import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Excel Data Statistical Analyzer", layout="wide")

st.title("📊 Excel Data Statistical Analyzer")

uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    st.subheader("📈 Numeric Columns Distribution")
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    for col in numeric_cols:
        fig = px.histogram(df, x=col, nbins=30, title=f"Distribution of {col}")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📦 Box Plots (Outlier Detection)")
    for col in numeric_cols:
        fig = px.box(df, y=col, title=f"Box plot of {col}")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔗 Correlation Heatmap")
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        st.pyplot(fig)

    st.subheader("📊 Categorical Pie Charts")
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    for col in cat_cols:
        if df[col].nunique() < 10:
            fig = px.pie(df, names=col, title=f"Pie chart of {col}")
            st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Please upload a file to start analysis.")
