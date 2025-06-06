import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time

# Setup Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("iot-irrigation-dashboard-f5014770d38d.json", scope)
client = gspread.authorize(creds)


# Buka spreadsheet
spreadsheet = client.open_by_key("19dRpsMDpz8EcSnyIYVz_fYjnz55-Id1j5SHZzzTBTnE")  # Ganti dengan ID spreadsheet kamu
sheet = spreadsheet.sheet1

# Ambil data
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Streamlit Dashboard
st.title("📊 IoT Irrigation Dashboard")

# Menampilkan nilai terbaru sensor
if not df.empty:
    latest_data = df.iloc[-1]
    waktu = latest_data["Waktu"]
    soil = latest_data["Kelembaban Tanah"]
    temp = latest_data["Suhu"]
    hum = latest_data["Kelembaban Udara"]
    status_tanah = latest_data.get("Status Tanah", "Tidak tersedia")

    st.write("### 📌 Data Terbaru Sensor")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌱 Kelembaban Tanah", f"{soil} %")
    with col2:
        st.metric("🌡 Suhu", f"{temp} °C")
    with col3:
        st.metric("💧 Kelembaban Udara", f"{hum} %")
    with col4:
        st.metric("📍 Status Tanah", status_tanah)

# Menampilkan tabel data sensor
st.write("### 🔍 Data Sensor")
st.dataframe(df)

# Grafik kelembaban tanah
st.write("### 📈 Grafik Kelembaban Tanah")
st.line_chart(df["Kelembaban Tanah"])

# Grafik suhu & kelembaban udara
st.write("### 🌡️ Grafik Suhu & Kelembaban Udara")
st.line_chart(df[["Suhu", "Kelembaban Udara"]])

# Auto refresh
st.write("⏳ Dashboard akan diperbarui otomatis setiap 5 detik...")
time.sleep(5)
st.rerun()
