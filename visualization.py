import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #667eea, #764ba2);
    color: white;
}
h1, h2, h3 {
    text-align: center;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🚢 Titanic Data Analysis Dashboard")

file = st.file_uploader("Upload CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    df["Age"] = df["Age"].fillna(df["Age"].mean())

    gender = st.selectbox("Select Gender", df["Sex"].dropna().unique())
    df = df[df["Sex"] == gender]

    st.sidebar.title("Navigation")
    option = st.sidebar.selectbox(
        "Choose option",
        ["Data Preview", "Charts", "Advanced Charts"]
    )

    st.sidebar.subheader("Filter Data")

    age = st.sidebar.slider(
        "Select Age",
        int(df["Age"].min()),
        int(df["Age"].max())
    )
    df = df[df["Age"] <= age]

    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        "Download Data",
        csv,
        "filtered_data.csv",
        "text/csv"
    )

    if option == "Data Preview":
        st.subheader("Data Preview")
        st.dataframe(df)

        st.subheader("Summary Statistics")
        st.write(df.describe())

        st.subheader("Quick Stats")
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Rows", df.shape[0])
        col2.metric("Total Columns", df.shape[1])
        col3.metric("Average Age", int(df["Age"].mean()))

    elif option == "Charts":
        numeric_columns = df.select_dtypes(include=['number']).columns
        column = st.selectbox("Choose column", numeric_columns)

        st.subheader("Line Chart")
        st.plotly_chart(px.line(df, y=column))

        st.subheader("Bar Chart")
        st.plotly_chart(px.bar(df, y=column))

        st.subheader("Histogram")
        st.plotly_chart(px.histogram(df, x=column))

    elif option == "Advanced Charts":
        st.subheader("Scatter Plot")

        numerical_columns = df.select_dtypes(include=['number']).columns.tolist()

        x_column = st.selectbox("X axis", numerical_columns)
        y_column = st.selectbox("Y axis", numerical_columns)
        color = st.selectbox("Color", df.columns)

        fig = px.scatter(df, x=x_column, y=y_column, color=color)
        st.plotly_chart(fig)

        st.subheader("Pie Chart")
        pie_column = st.selectbox("Choose column for pie", df.columns)
        st.plotly_chart(px.pie(df, names=pie_column))

    st.subheader("Survival Rate")
    st.plotly_chart(px.pie(df, names="Survived", title="Survival Distribution"))

    st.subheader("Gender Distribution")
    st.plotly_chart(px.bar(df, x="Sex", title="Male vs Female Count"))

    st.subheader("AI Insight")

    survival_rate = df["Survived"].mean()
    st.success(f"Survival Rate: {round(survival_rate * 100, 2)}%")

    if survival_rate > 0.5:
        st.success("Most passengers survived")
    else:
        st.error("Most passengers did NOT survive")

    female_survival = df[df["Sex"] == "female"]["Survived"].mean()
    male_survival = df[df["Sex"] == "male"]["Survived"].mean()

    if female_survival > male_survival:
        st.info("Females had higher survival rate")
    else:
        st.info("Males had higher survival rate")

    st.success("Analysis Done Successfully!")