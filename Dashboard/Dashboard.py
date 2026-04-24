import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

file_path = "bike_df.csv"
bike_df = pd.read_csv(file_path)

st.title("🚲 Bike Sharing Dataset — Capital Bikeshare, Washington D.C.")

# Sidebar untuk navigasi dan eksplorasi data
with st.sidebar:
    st.title('Dashboard')
    
    st.subheader("🔍 Eksplorasi Data")
    show_summary = st.toggle("Tampilkan Ringkasan Informasi", value=True)
    show_first_rows = st.toggle("Tampilkan Lima Baris Pertama", value=True)
    show_duplicates = st.toggle("Periksa Duplikasi", value=True)
    show_statistics = st.toggle("Tampilkan Statistik", value=True)
    show_visualizations = st.toggle("Tampilkan Visualisasi", value=True)
    st.divider()


from sidebar import show_sidebar
from dataset_summary import show_dataset_summary

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# Panggil sidebar — hasilnya berisi semua nilai filter
filters = show_sidebar()
if show_summary:
    show_dataset_summary()

if show_first_rows:      
    st.header("Lima Baris Pertama DataFrame")
    st.write(bike_df.head())

if show_duplicates:
    st.header("Periksa Duplikasi")
    num_duplicates = bike_df.duplicated().sum()
    st.write(f"Jumlah Duplikasi: {num_duplicates}")

if show_statistics:
    st.header("Ringkasan Statistik DataFrame")
    st.write(bike_df.describe())

if show_visualizations:
    st.header("Visualisasi Data")
    # Filter tahun 2012
    df_2012 = bike_df[bike_df['yr_day'] == 1].copy()

    # Hitung rata-rata per jam
    hourly_user = (
        df_2012.groupby('hr')[['casual_day','registered_day']]
        .mean()
        .reset_index()
    )

    # Hitung rasio (indikasi peluang konversi)
    hourly_user['conversion_opportunity'] = hourly_user['casual_day'] / (hourly_user['registered_day'] + 1)

    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)

    # Plot casual_day & registered_day
    sns.lineplot(data=hourly_user, x='hr', y='casual_day', marker='o', label='Casual Users')
    sns.lineplot(data=hourly_user, x='hr', y='registered_day', marker='o', label='Registered Users')

    # 🔴 Anotasi Peak Casual (waktu terbaik)
    peak_idx = hourly_user['casual_day'].idxmax()
    peak_hr = hourly_user.loc[peak_idx, 'hr']
    peak_val = hourly_user.loc[peak_idx, 'casual_day']

    plt.scatter(peak_hr, peak_val, color='red', zorder=3)
    plt.annotate(
        f'Peak Casual\nJam {int(peak_hr)}\n{int(peak_val)}',
        xy=(peak_hr, peak_val),
        xytext=(peak_hr+0.5, peak_val*1.1),
        arrowprops=dict(arrowstyle='->'),
        fontsize=9
    )

    # Highlight area peluang konversi tinggi (casual tinggi, registered rendah)
    plt.fill_between(
        hourly_user['hr'],
        hourly_user['casual_day'],
        hourly_user['registered_day'],
        where=(hourly_user['casual_day'] > hourly_user['registered_day']),
        color='green',
        alpha=0.1,
        label='Peluang Konversi Tinggi'
    )

    # Label & style
    ax.set_title('Identifikasi Waktu Optimal Konversi Casual ke Registered (2012)', fontsize=14)
    ax.set_xlabel('Jam (0–23)')
    ax.set_ylabel('Rata-rata Penyewaan')
    ax.set_xticks(range(0,24))
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()

    plt .tight_layout()
    st.pyplot(fig)

    # Mapping tahun
    bike_df['year'] = bike_df['yr_day'].map({
        0: '2011',
        1: '2012'
    })

    # Mapping kondisi cuaca agar mudah dipahami
    weather_map = {
        'Clear': 'Cerah',
        'Cloudy': 'Berawan',
        'Light Rain': 'Hujan Ringan',
        'Heavy Rain': 'Hujan Lebat',
        1: 'Cerah',
        2: 'Berawan / Berkabut',
        3: 'Hujan Ringan',
        4: 'Hujan Lebat'
    }

    bike_df['weather_label'] = bike_df['weathersit_day'].map(weather_map)

    # Hitung rata-rata penyewaan berdasarkan jam, tahun, dan cuaca
    weather_hour_year = (
        bike_df
        .groupby(['hr', 'year', 'weather_label'])['cnt_day']
        .mean()
        .reset_index()
    )

    # Plot
    g = sns.relplot(
        data=weather_hour_year,
        x='hr',
        y='cnt_day',
        hue='weather_label',
        col='year',
        kind='line',
        marker='o',
        height=5,
        aspect=1.3
    )

    # Highlight jam sibuk
    for ax in g.axes.flat:
        ax.axvspan(7, 9, color='orange', alpha=0.15)
        ax.axvspan(17, 19, color='orange', alpha=0.15)
        ax.set_xticks(range(0, 24, 2))
        ax.grid(True, linestyle='--', alpha=0.4)

    g.set_axis_labels('Jam dalam Sehari', 'Rata-rata Penyewaan')
    g.set_titles('Tahun {col_name}')

    plt.suptitle(
        'Pengaruh Cuaca dan Jam terhadap Penyewaan Sepeda pada Tahun 2011 dan 2012',
        fontsize=14,
        y=1.05
    )

    st.pyplot(g)