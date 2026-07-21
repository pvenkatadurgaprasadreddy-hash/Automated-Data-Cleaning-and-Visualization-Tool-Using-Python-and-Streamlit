import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from cleaning import clean_data
from charts import show_charts


# ----------------------------
# PAGE CONFIGURATION
# ----------------------------
st.set_page_config(
    page_title="Data Cleaning Tool",
    page_icon="🧹",
    layout="wide"
)


# ----------------------------
# TITLE
# ----------------------------
st.title("🧹 Automated Data Cleaning & Visualization Tool")
st.markdown("### Built using Python, Pandas & Streamlit")
st.info(
    "This application helps users clean CSV datasets by removing duplicate rows, "
    "handling missing values, removing unnecessary spaces, and generating "
    "interactive visualizations for better data analysis."
)

st.write("Upload a CSV file and automatically clean your data.")

st.divider()


# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("⚙️ Data Cleaning Options")

remove_duplicates = st.sidebar.checkbox(
    "Remove Duplicate Rows",
    value=True
)

fill_missing = st.sidebar.checkbox(
    "Fill Missing Values",
    value=True
)

strip_spaces = st.sidebar.checkbox(
    "Remove Extra Spaces",
    value=True
)

drop_empty = st.sidebar.checkbox(
    "Remove Empty Rows",
    value=False
)

st.sidebar.markdown("---")
st.sidebar.info("Developed using Python & Streamlit")


# ----------------------------
# FILE UPLOAD
# ----------------------------
uploaded_file = st.file_uploader(
    "📂 Upload CSV File",
    type=["csv"]
)


if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("✅ File Uploaded Successfully!")


    # ----------------------------
    # ORIGINAL DATA
    # ----------------------------
    st.subheader("📋 Original Dataset")
    st.dataframe(df, use_container_width=True)


    # ----------------------------
    # CLEAN DATA
    # ----------------------------
    cleaned_df, rows_before, rows_after = clean_data(
        df,
        remove_duplicates,
        fill_missing,
        strip_spaces,
        drop_empty
    )


    # ----------------------------
    # SUMMARY
    # ----------------------------
    st.subheader("📊 Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Rows Before",
        rows_before
    )

    col2.metric(
        "Rows After",
        rows_after
    )

    col3.metric(
        "Rows Removed",
        rows_before - rows_after
    )


    # ----------------------------
    # CLEANED DATA
    # ----------------------------
    st.subheader("✅ Cleaned Dataset")
    st.dataframe(cleaned_df, use_container_width=True)


    # ----------------------------
    # COLUMN INFORMATION
    # ----------------------------
    st.subheader("📌 Column Information")

    info = pd.DataFrame({
        "Column": cleaned_df.columns,
        "Datatype": cleaned_df.dtypes.astype(str),
        "Missing Values": cleaned_df.isnull().sum().values
    })

    st.dataframe(info, use_container_width=True)


    # ----------------------------
    # STATISTICS
    # ----------------------------
    st.subheader("📈 Statistical Summary")

    st.dataframe(
        cleaned_df.describe(include="all")
    )


    # ----------------------------
    # VISUALIZATION
    # ----------------------------
    show_charts(cleaned_df)


    # ----------------------------
    # MISSING VALUES CHART
    # ----------------------------
    st.subheader("📉 Missing Values")

    missing = cleaned_df.isnull().sum()

    fig, ax = plt.subplots(figsize=(8, 4))

    missing.plot(
        kind="bar",
        ax=ax
    )

    ax.set_ylabel("Missing Count")

    st.pyplot(fig)


    # ----------------------------
    # DOWNLOAD
    # ----------------------------
    csv = cleaned_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="📥 Download Cleaned CSV",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )


else:

    st.info("📂 Please upload a CSV file.")