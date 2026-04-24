import streamlit as st

def show_dataset_summary():

    # ── Header ────────────────────────────────────────────────────────────────
    st.caption(
        "Data historis penyewaan sepeda tahun 2011–2012 dari sistem Capital Bikeshare, "
        "tersedia dalam agregasi per jam dan per hari."
    )

    st.divider()

    # ── Metric Cards ──────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records (Hourly)", "17.379", "jam")
    col2.metric("Total Records (Daily)",  "731",    "hari")
    col3.metric("Periode Data",           "2",      "tahun")
    col4.metric("Total Fitur",            "16",     "kolom")

    st.divider()

    # ── Info Cards ────────────────────────────────────────────────────────────
    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            st.markdown("**Fitur Waktu & Kalender**")
            data_waktu = {
                "Fitur": ["dteday", "yr", "season", "mnth", "hr", "weekday", "workingday", "holiday"],
                "Keterangan": [
                    "Tanggal",
                    "Tahun (0=2011, 1=2012)",
                    "Musim (1=Spring, 2=Summer, 3=Fall, 4=Winter)",
                    "Bulan (1–12)",
                    "Jam (0–23) — hanya hour.csv",
                    "Hari dalam seminggu (0–6)",
                    "1 jika bukan weekend/holiday",
                    "1 jika hari libur",
                ],
            }
            st.dataframe(data_waktu, hide_index=True, use_container_width=True)

        with st.container(border=True):
            st.markdown("**Fitur Target (Output)**")
            data_target = {
                "Kolom":      ["casual",   "registered",         "cnt"],
                "Keterangan": [
                    "Jumlah pengguna tidak terdaftar",
                    "Jumlah pengguna terdaftar",
                    "Total sewa (casual + registered)",
                ],
            }
            st.dataframe(data_target, hide_index=True, use_container_width=True)

    with right:
        with st.container(border=True):
            st.markdown("**Fitur Cuaca & Lingkungan**")
            data_cuaca = {
                "Fitur":      ["weathersit", "temp",     "atemp",        "hum",          "windspeed"],
                "Keterangan": [
                    "Kondisi cuaca (1–4)",
                    "Suhu normalized (÷41°C)",
                    "Suhu terasa normalized (÷50°C)",
                    "Kelembaban normalized (÷100)",
                    "Kecepatan angin normalized (÷67)",
                ],
            }
            st.dataframe(data_cuaca, hide_index=True, use_container_width=True)

        with st.container(border=True):
            st.markdown("**Kode Kondisi Cuaca (weathersit)**")
            data_weathersit = {
                "Kode": ["1", "2", "3", "4"],
                "Label": ["Cerah / Sedikit berawan", "Berkabut / Berawan",
                          "Salju / Hujan ringan", "Hujan lebat / Badai"],
                "Dampak": ["Tertinggi ✅", "Sedang 🔵", "Rendah 🟡", "Sangat rendah 🔴"],
            }
            st.dataframe(data_weathersit, hide_index=True, use_container_width=True)

    st.divider()

    # ── Task Tags ─────────────────────────────────────────────────────────────
    st.markdown("**Task yang Dapat Dilakukan**")
    tags = st.columns(5)
    label = [
        "📈 Regresi prediksi sewa",
        "🔍 Deteksi anomali & event",
        "🌤️ Analisis pengaruh cuaca",
        "👥 Segmentasi pengguna",
        "🕐 Analisis pola waktu & musim",
    ]
    for col, text in zip(tags, label):
        col.info(text)

    # ── Source Footer ─────────────────────────────────────────────────────────
    st.caption(
        "Sumber: Fanaee-T, Hadi & Gama, Joao — *Event labeling combining ensemble detectors "
        "and background knowledge*, Progress in Artificial Intelligence (2013), Springer Berlin Heidelberg. "
        "| Data: capitalbikeshare.com | Cuaca: freemeteo.com"
    )


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    st.set_page_config(
        page_title="Bike Sharing Dashboard",
        page_icon="🚲",
        layout="wide",
    )
    show_dataset_summary()
