import os
import uuid

import pandas as pd
import streamlit as st

from report_tool import csv_to_report

st.title("CSV to Excel Report")

uploaded = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded is not None:
    output_file = f"report_{uuid.uuid4()}.xlsx"

    try:
        df = pd.read_csv(uploaded)

        if df.empty:
            st.warning("That file has headers but no data rows.")
            st.stop()

        st.write("Original Data")
        st.dataframe(df)

        uploaded.seek(0)
        csv_to_report(uploaded, output_file)

        cleaned_preview = pd.read_excel(output_file).iloc[:-1]

        with open(output_file, "rb") as file:
            report_bytes = file.read()

        col1, col2 = st.columns(2)
        col1.metric("Rows before", len(df))
        col2.metric("Rows after", len(cleaned_preview))

        st.write("Cleaned Data")
        st.dataframe(cleaned_preview)

        st.download_button(
            label="Download Excel Report",
            data=report_bytes,
            file_name="report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    except pd.errors.EmptyDataError:
        st.error("That file is empty. Please upload a CSV that contains data.")
    except Exception:
        st.error("Something went wrong reading that file. Please ensure it is a valid CSV.")
    finally:
        if os.path.exists(output_file):
            os.remove(output_file)