import streamlit as st

def show_sidebar():
    with st.sidebar:
        


        # ── Info Dataset ──────────────────────────────────────────────────────
        st.markdown("### 📋 Info Dataset")
        st.markdown(
            """
            | Keterangan | Nilai |
            |---|---|
            | Sumber | Capital Bikeshare |
            | Kota | Washington D.C. |
            | Periode | 2011 – 2012 |
            | Records | 17.379 (jam) |
            | Fitur | 16 kolom |
            """,
        )

        st.divider()

        # ── Footer ────────────────────────────────────────────────────────────
        st.caption("📚 Dataset: Fanaee-T & Gama (2013)")
        st.caption("Dibuat untuk keperluan analisis akademik.")

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    st.set_page_config(
        page_title="Bike Sharing Dashboard",
        page_icon="🚲",
        layout="wide",
    )