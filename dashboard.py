import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi warna tema
st.set_page_config(
    page_title="Dashboard Analisis Data Sepeda",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Definisi warna tema
COLOR_PRIMARY = "#98c1d9"
COLOR_SECONDARY = "#3d5a80"
COLOR_ACCENT = "#ee6c4d"
COLOR_BACKGROUND = "#e0fbfc"
COLOR_TEXT = "#293241"

# Style CSS
st.markdown(
    f"""
    <style>
        body {{
            color: {COLOR_TEXT};
            background-color: {COLOR_BACKGROUND};
        }}
        .st-emotion-cache-10trblm {{
            color: {COLOR_TEXT};
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {COLOR_SECONDARY};
        }}
        .st-emotion-cache-j5r0tf {{
             background-color: {COLOR_BACKGROUND};
        }}
        .st-emotion-cache-1avcm0n, .st-emotion-cache-hxt7ib {{
             background-color: {COLOR_BACKGROUND};
             color: {COLOR_TEXT};
        }}
        .st-emotion-cache-10trblm {{
            background-color: {COLOR_BACKGROUND};
             color: {COLOR_TEXT};
        }}
        .st-emotion-cache-16txtl3, .st-emotion-cache-10trblm, .st-emotion-cache-19rxj2a {{
            color: {COLOR_TEXT};
        }}
        .st-emotion-cache-1w61f3y  {{
             background-color: {COLOR_PRIMARY};
        }}
        .st-emotion-cache-5668if, .st-emotion-cache-54y18v {{
           background-color: {COLOR_PRIMARY};
        }}
        .st-emotion-cache-1v1h437 {{
           background-color: {COLOR_PRIMARY};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    df1 = pd.read_csv("clean_df_day.csv")
    # Contoh data dummy untuk df2 (Ganti ini dengan data CSV kedua Anda)
    data2 = {
        'kategori': ['A', 'B', 'C', 'A', 'B', 'C'],
        'nilai': [10, 20, 15, 25, 30, 22]
    }
    df2 = pd.DataFrame(data2)
    return df1, df2

# Load data
df1, df2 = load_data()

# Judul aplikasi
st.title("🚲 Dashboard Analisis Data Sepeda dan Data Lainnya")

# Deskripsi singkat
st.write("Dashboard ini menampilkan visualisasi data penyewaan sepeda harian dan data lainnya.")

# Sidebar untuk filter
with st.sidebar:
  st.header("Filter Data")

  # Filter untuk musim (df1)
  musim_pilihan = st.multiselect(
      "Pilih Musim",
      options=df1['season'].unique(),
      default=df1['season'].unique()
  )

  # Filter untuk bulan (df1)
  bulan_pilihan = st.multiselect(
      "Pilih Bulan",
      options=df1['mnth'].unique(),
      default=df1['mnth'].unique()
  )

  # Filter untuk tahun (df1)
  tahun_pilihan = st.multiselect(
      "Pilih Tahun",
      options=df1['yr'].unique(),
      default=df1['yr'].unique()
  )

  st.markdown("---")

  st.header("Informasi Tambahan")
  st.write("Data ini adalah contoh data untuk visualisasi.")

# Filter data berdasarkan pilihan
df1_filtered = df1[
    df1['season'].isin(musim_pilihan) &
    df1['mnth'].isin(bulan_pilihan) &
    df1['yr'].isin(tahun_pilihan)
]

# Menampilkan Matriks Metrik
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Penyewaan", value=df1_filtered['cnt'].sum())
with col2:
    st.metric(label="Rata-rata Penyewaan", value=round(df1_filtered['cnt'].mean(), 2))
with col3:
    st.metric(label="Jumlah Hari", value=df1_filtered['dteday'].nunique())

# Tampilan Grafik 1 (df1)
st.header("Grafik Penyewaan Sepeda per Hari")

# Visualisasi jumlah penyewaan sepeda per hari
fig_cnt_per_day = px.line(
    df1_filtered, 
    x='dteday', 
    y='cnt', 
    title='Total Penyewaan Sepeda Harian',
    color_discrete_sequence=[COLOR_ACCENT]
)
st.plotly_chart(fig_cnt_per_day, use_container_width=True)

# Tampilan Grafik 2 (df1)
st.header("Grafik Penyewaan Sepeda per Musim")
# Visualisasi penyewaan per musim
fig_cnt_per_season = px.bar(
    df1_filtered.groupby('season')['cnt'].sum().reset_index(),
    x='season',
    y='cnt',
    title='Total Penyewaan Sepeda per Musim',
    labels={'cnt': 'Total Penyewaan', 'season': 'Musim'},
    color_discrete_sequence=[COLOR_PRIMARY]
)
st.plotly_chart(fig_cnt_per_season, use_container_width=True)



# Menampilkan Dataframe
st.header("Data Tabel Sepeda Harian")
st.dataframe(df1_filtered.head().style.background_gradient(cmap='Blues'))

# Catatan kaki
st.markdown("---")
st.write("Dibuat dengan Streamlit")
