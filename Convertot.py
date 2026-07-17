import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="API to CSV Dashboard", layout="wide")
st.title("📊 API JSON to CSV Dashboard")
st.write("Enter the API URL. The data will be retrieved and converted into a CSV file.")
api_url = st.text_input("🔗 API URL:", placeholder="https://example.com/api/data")
if st.button("▶ Fetch Data"):
    if not api_url:
        st.warning("Please enter the API URL.")
    else:
        try:
            response = requests.get(api_url, timeout=30)
            if response.status_code != 200:
                st.error(f"API Fetch Error: {response.status_code}")
            else:
                json_data = response.json()
                records = json_data.get("data", [])
                if not records:
                    st.warning("No data is available in the API.")
                else:
                    df = pd.DataFrame(records)
                    columns = [
                        "key",
                        "volume",
                        "num_txs"
                    ]
                    df = df[
                        [
                            col for col in columns
                            if col in df.columns
                        ]
                    ]
                    st.success(f"✅ Successfully retrieved {len(df)} records.")
                    st.subheader("📋 Records Table")
                    st.dataframe(df, use_container_width=True)
                    st.subheader("ℹ️ API Information")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(
                            "Total",
                            json_data.get(
                                "total",
                                0
                            )
                        )
                    with col2:
                        st.metric(
                            "Time spent",
                            json_data.get(
                                "time_spent",
                                0
                            )
                        )
                    st.subheader("⬇️ Download CSV")
                    default_filename = (
                        f"api_export_"
                        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    )
                    filename = st.text_input("CSV File Name:", value=default_filename)
                    if not filename.endswith(".csv"):
                        filename += ".csv"
                    csv_data = df.to_csv(index=False, encoding="utf-8")
                    st.download_button(label="📥 Download CSV File", data=csv_data, file_name=filename, mime="text/csv")
        except requests.exceptions.Timeout:
            st.error("⏳ API request timed out.")
        except requests.exceptions.RequestException as e:
            st.error(f"API connection error:\n{e}")
        except Exception as e:
            st.error(f"Data processing error:\n{e}")
