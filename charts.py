import streamlit as st
import plotly.express as px
import pandas as pd


def show_charts(df):

    st.subheader("📊 Interactive Charts")

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if len(numeric_columns) == 0:
        st.warning("No numeric columns found.")
        return

    chart_type = st.selectbox(
        "Select Chart Type",
        [
            "Histogram",
            "Bar Chart",
            "Line Chart",
            "Scatter Plot",
            "Box Plot",
            "Pie Chart",
            "Correlation Heatmap"
        ]
    )


    # ----------------------------
    # CORRELATION HEATMAP
    # ----------------------------
    if chart_type == "Correlation Heatmap":

        if len(numeric_columns) < 2:
            st.warning(
                "Need at least two numeric columns for correlation heatmap."
            )
            return

        correlation = df[numeric_columns].corr()

        fig = px.imshow(
            correlation,
            text_auto=True,
            title="🔥 Correlation Heatmap",
            color_continuous_scale="RdBu"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        return


    column = st.selectbox(
        "Select Numeric Column",
        numeric_columns
    )


    if chart_type == "Histogram":

        fig = px.histogram(
            df,
            x=column,
            title=f"Histogram of {column}"
        )

        st.plotly_chart(fig, use_container_width=True)


    elif chart_type == "Bar Chart":

        counts = df[column].value_counts().reset_index()

        counts.columns = [column, "Count"]

        fig = px.bar(
            counts,
            x=column,
            y="Count",
            title=f"Bar Chart of {column}"
        )

        st.plotly_chart(fig, use_container_width=True)


    elif chart_type == "Line Chart":

        fig = px.line(
            df,
            y=column,
            title=f"Line Chart of {column}"
        )

        st.plotly_chart(fig, use_container_width=True)


    elif chart_type == "Scatter Plot":

        second_column = st.selectbox(
            "Select Second Column",
            numeric_columns
        )

        fig = px.scatter(
            df,
            x=column,
            y=second_column,
            title=f"{column} vs {second_column}"
        )

        st.plotly_chart(fig, use_container_width=True)


    elif chart_type == "Box Plot":

        fig = px.box(
            df,
            y=column,
            title=f"Box Plot of {column}"
        )

        st.plotly_chart(fig, use_container_width=True)


    elif chart_type == "Pie Chart":

        counts = df[column].value_counts().reset_index()

        counts.columns = [column, "Count"]

        fig = px.pie(
            counts,
            names=column,
            values="Count",
            title=f"Pie Chart of {column}"
        )

        st.plotly_chart(fig, use_container_width=True)