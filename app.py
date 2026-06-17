import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pickle
import json
import base64

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="Peluang Kesejahteraan", page_icon="📊", layout="wide")

# --- PALET WARNA ---
COLOR_BG = "#0f111e"       
COLOR_BROWN = "#73472a"    
COLOR_CREAM = "#f4d4a8"    
PETA_COLORS = {
    "Kemiskinan Rendah": "#f0dcbe", 
    "Kemiskinan Sedang": "#e3a665", 
    "Kemiskinan Tinggi": "#c7724b", 
    "Kemiskinan Sangat Tinggi": "#a33c3b"
}

# ==========================================
# 1. FUNGSI PEMUAT DATA & ASET
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv('datasetfinal_visdat.csv')
    conditions = [(df['Kemiskinan'] < 10), (df['Kemiskinan'] >= 10) & (df['Kemiskinan'] < 20), (df['Kemiskinan'] >= 20) & (df['Kemiskinan'] < 30), (df['Kemiskinan'] >= 30)]
    choices = ['Kemiskinan Rendah', 'Kemiskinan Sedang', 'Kemiskinan Tinggi', 'Kemiskinan Sangat Tinggi']
    df['Kategori_Kemiskinan'] = np.select(conditions, choices, default='Tidak Terdefinisi')
    df['Nama_Daerah_Peta'] = df['Nama_Daerah'].str.title() 
    return df

@st.cache_data
def load_geojson():
    with open('kabupaten-kota-sinkron.json', 'r') as f:
        return json.load(f)

@st.cache_resource
def load_model():
    with open('model_kemiskinan_fiks.pkl', 'rb') as file:
        return pickle.load(file)

@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    df = load_data()
    geojson_indonesia = load_geojson()
    model = load_model()
except FileNotFoundError as e:
    st.error(f"Error: {e}. Pastikan file CSV, JSON, dan PKL ada di folder project!")
    st.stop()

# ==========================================
# 2. CSS CUSTOM (LOGO AESTHETIC & FULL WIDTH)
# ==========================================
try:
    img_b64 = get_base64_of_bin_file('hero_bg.jpg')
    bg_image_css = f"background-image: linear-gradient(rgba(15, 17, 30, 0.75), rgba(15, 17, 30, 0.85)), url('data:image/jpg;base64,{img_b64}');"
except FileNotFoundError:
    bg_image_css = f"background-color: {COLOR_BROWN};"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@400;500;700;800;900&display=swap');

/* KUNCI UTAMA ANTI GESER SAMPING */
html, body {{
    overflow-x: hidden !important;
    max-width: 100% !important;
}}

/* MANTRA SMOOTH SCROLLING & GLOBAL FONT */
html, body, [class*="stApp"], [data-testid="stAppViewContainer"], .main, p, span, div {{
    scroll-behavior: smooth !important;
    font-family: 'Inter', sans-serif !important;
}}

h1, h2, h3, h4, h5, h6, .hero-title, .nav-logo {{
    font-family: 'Montserrat', sans-serif !important;
}}

/* MENGHANCURKAN TEMBOK PADDING STREAMLIT SECARA TOTAL */
header {{ visibility: hidden !important; display: none !important; }}
[data-testid="stAppViewContainer"] {{ padding: 0 !important; overflow-x: hidden !important; }}
[data-testid="block-container"], [data-testid="stAppViewBlockContainer"] {{ 
    padding-left: 0 !important; 
    padding-right: 0 !important; 
    padding-top: 0 !important; 
    padding-bottom: 0 !important; 
    max-width: 100% !important; 
    overflow-x: hidden !important; 
}}

/* HEADER NAVBAR PUTIH ESIK */
.nav-header {{ 
    position: fixed; top: 0; left: 0; width: 100%; 
    background-color: rgba(255, 255, 255, 0.95); 
    backdrop-filter: blur(10px); display: flex; justify-content: space-between; align-items: center;
    padding: 15px 5%; z-index: 99999; border-bottom: 1px solid #e0e0e0; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    box-sizing: border-box; 
}}
/* LOGO DIUBAH MENJADI AESTHETIC FORMAL (TIDAK BOLD) */
.nav-logo {{ 
    font-size: 1.4rem; 
    font-weight: 500; /* Diubah dari 900 ke 500 agar lebih elegan/tidak bold */
    color: {COLOR_BROWN}; 
    letter-spacing: 1.2px; /* Ditambah jarak huruf agar terlihat premium */
    display: flex; 
    align-items: center; 
    gap: 10px; 
}}
.nav-links a {{ color: {COLOR_BROWN}; text-decoration: none; margin-left: 30px; font-size: 1.05rem; font-weight: 600; transition: 0.3s; }}
.nav-links a:hover {{ color: {COLOR_BG}; text-decoration: none; border-bottom: 2px solid {COLOR_BG}; }}

/* HERO SECTION */
.hero-wrapper {{
    {bg_image_css}
    background-size: cover; background-position: center; 
    width: 100vw;
    position: relative;
    left: 50%;
    right: 50%;
    margin-left: -50vw;
    margin-right: -50vw;
    margin-top: -100px; 
    padding-top: 100px; 
    min-height: 100vh; 
    display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; 
    padding-left: 20px; padding-right: 20px; box-sizing: border-box; border-bottom: 5px solid {COLOR_BROWN};
    overflow: hidden;
}}
.hero-title {{ color: {COLOR_CREAM}; font-size: 4.5rem; font-weight: 900; margin-bottom: 20px; line-height: 1.2; text-shadow: 2px 4px 15px rgba(0,0,0,0.7); }}
.hero-subtitle {{ color: #ffffff; font-size: 1.4rem; max-width: 900px; margin: 0 auto; line-height: 1.7; text-shadow: 1px 2px 10px rgba(0,0,0,0.8); font-weight: 400; }}
.btn-hero {{ display: inline-block; margin-top: 40px; padding: 15px 40px; background-color: {COLOR_CREAM}; color: {COLOR_BROWN} !important; text-decoration: none; font-size: 1.1rem; font-weight: 800; border-radius: 50px; transition: 0.4s; border: 2px solid {COLOR_CREAM}; box-shadow: 0 4px 15px rgba(0,0,0,0.5); font-family: 'Montserrat', sans-serif !important; }}
.btn-hero:hover {{ background-color: transparent; color: {COLOR_CREAM} !important; transform: translateY(-3px); box-shadow: 0 10px 20px rgba(244, 212, 168, 0.3); }}

/* Pembungkus konten bawah */
.content-wrapper {{ padding: 0 6%; overflow-x: hidden; }}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. MENU HEADER & HERO SECTION
# ==========================================
st.markdown(f"""
<div id="beranda"></div>
<div class="nav-header">
    <div class="nav-logo">Peluang Kesejahteraan</div>
    <div class="nav-links">
        <a href="#beranda" target="_self">Beranda</a>
        <a href="#peta" target="_self">Peta Interaktif</a>
        <a href="#analisis" target="_self">Analisis Data</a>
        <a href="#simulator" target="_self">Simulator Kebijakan</a>
    </div>
</div>

<div class="hero-wrapper">
    <h1 class="hero-title">Mengukur Dampak Pendidikan<br>Terhadap Kesejahteraan</h1>
    <p class="hero-subtitle">Jelajahi korelasi antara Rata-rata Lama Sekolah (RLS) dan tingkat kemiskinan di 515 wilayah Kabupaten/Kota di Indonesia, serta simulasikan target kebijakan berbasis data.</p>
    <a href="#analisis" target="_self" class="btn-hero">Lihat Insight Data &darr;</a>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. PETA SPASIAL
# ==========================================
st.markdown("<div class='content-wrapper'>", unsafe_allow_html=True)

st.markdown("<div id='peta' style='padding-top: 100px; margin-top: -60px;'></div>", unsafe_allow_html=True) 
st.markdown(f"<h2 style='text-align: center; color: {COLOR_CREAM}; margin-bottom: 30px; font-weight: 800;'>Eksplorasi Peta Kesejahteraan Indonesia</h2>", unsafe_allow_html=True)

with st.spinner("Merender visualisasi spasial..."):
    fig_map = px.choropleth_map(
        df, geojson=geojson_indonesia, locations='Nama_Daerah_Peta', featureidkey='properties.NAME_2',
        color='Kategori_Kemiskinan', color_discrete_map=PETA_COLORS, map_style="carto-darkmatter",
        zoom=4.0, center={"lat": -2.5, "lon": 118.0}, opacity=0.9,
        hover_name='Nama_Daerah', hover_data={'Nama_Daerah_Peta': False, 'Kemiskinan': True, 'RLS': True, 'IPM': True}
    )
    fig_map.update_traces(marker_line_width=0.5, marker_line_color="#333333") 
    
    fig_map.for_each_trace(lambda t: t.update(
        hoverlabel=dict(
            bgcolor=PETA_COLORS.get(t.name, COLOR_BG),
            bordercolor="#333333",
            font=dict(
                color="#ffffff" if "Tinggi" in str(t.name) else "#333333",
                family="Inter, sans-serif",
                size=13
            )
        )
    ))

    fig_map.update_layout(plot_bgcolor=COLOR_BG, paper_bgcolor=COLOR_BG, font=dict(family="Inter, sans-serif", color="#ffffff"), margin=dict(l=0, r=0, t=0, b=0), height=550)
    st.plotly_chart(fig_map, use_container_width=True)

st.markdown("<br><hr style='border: 1px solid #333; margin: 50px 0;'>", unsafe_allow_html=True)

# ==========================================
# 5. INSIGHT BERBASIS DATA 
# ==========================================
st.markdown("<div id='analisis' style='padding-top: 100px; margin-top: -60px;'></div>", unsafe_allow_html=True) 
st.markdown(f"<h2 style='text-align: center; color: {COLOR_CREAM}; margin-bottom: 40px; font-weight: 800;'>Insight Berbasis Data</h2>", unsafe_allow_html=True)

col_text, col_chart = st.columns([1, 1.3], gap="large")

with col_text:
    st.markdown(f"""
<div style='background-color: {COLOR_CREAM}; padding: 35px 30px; border-radius: 15px; color: {COLOR_BG}; box-shadow: 0 8px 20px rgba(0,0,0,0.3); height: 100%; border: 1px solid #d4b48a; box-sizing: border-box;'>
<p style='font-size: 1.15rem; line-height: 1.7; margin-bottom: 25px; font-weight: 500;'>
Mari kita bedah grafik di samping. Dari data ini, kita bisa melihat seberapa besar sebenarnya pengaruh sekolah terhadap kesejahteraan masyarakat.
</p>
<div style='margin-bottom: 20px;'>
<span style='font-size: 1.5rem; color: #5a3721; line-height: 1;'>&bull;</span> <span style='font-family: Montserrat, sans-serif; font-weight: 800; font-size: 1.15rem; color: #5a3721;'>Garis yang Menurun:</span><br>
<span style='font-size: 1.05rem; line-height: 1.6;'>Kalau kita perhatikan, garis trennya jelas menurun. Ini artinya sederhana: semakin lama rata-rata warga di suatu daerah bersekolah (RLS naik), angka kemiskinannya cenderung semakin berkurang.</span>
</div>
<div style='margin-bottom: 20px;'>
<span style='font-size: 1.5rem; color: #5a3721; line-height: 1;'>&bull;</span> <span style='font-family: Montserrat, sans-serif; font-weight: 800; font-size: 1.15rem; color: #5a3721;'>Dampak Nyata Pendidikan:</span><br>
<span style='font-size: 1.05rem; line-height: 1.6;'>Dari hitungan sistem, pendidikan terbukti bisa menekan angka kemiskinan. Setiap kali suatu daerah berhasil menambah rata-rata <b>1 tahun masa sekolah</b> warganya, kemiskinan di daerah tersebut diprediksi bisa turun sekitar <b>2,38%</b>.</span>
</div>
<div>
<span style='font-size: 1.5rem; color: #5a3721; line-height: 1;'>&bull;</span> <span style='font-family: Montserrat, sans-serif; font-weight: 800; font-size: 1.15rem; color: #5a3721;'>Bukan Satu-satunya Solusi:</span><br>
<span style='font-size: 1.05rem; line-height: 1.6;'>Walaupun penting, data menunjukkan bahwa pendidikan hanya memengaruhi sekitar <b>29,4%</b> tingkat kemiskinan. Sisanya yang <b>70,6%</b> membuktikan bahwa pemerintah juga harus membereskan faktor lain, seperti infrastruktur jalan dan lapangan pekerjaan.</span>
</div>
</div>
""", unsafe_allow_html=True)

with col_chart:
    fig_scatter = px.scatter(
        df, x="RLS", y="Kemiskinan", hover_name="Nama_Daerah", trendline="ols",
        labels={"RLS": "Rata-rata Lama Sekolah (Tahun)", "Kemiskinan": "Tingkat Kemiskinan (%)"},
        color_discrete_sequence=[COLOR_BROWN]
    )
    fig_scatter.update_traces(line=dict(color="#a33c3b", width=4), selector=dict(mode="lines")) 
    
    fig_scatter.update_layout(
        plot_bgcolor="#ffffff", 
        paper_bgcolor="#ffffff", 
        font=dict(family="Inter, sans-serif", color=COLOR_BG), 
        showlegend=False, 
        margin=dict(l=20, r=20, t=30, b=20), 
        height=550
    )
    
    fig_scatter.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='#e0e0e0', zeroline=False,
        title_font=dict(family="Montserrat, sans-serif", color=COLOR_BG, size=15, weight="bold"),
        tickfont=dict(family="Inter, sans-serif", color=COLOR_BG, size=13)
    )
    fig_scatter.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='#e0e0e0', zeroline=False,
        title_font=dict(family="Montserrat, sans-serif", color=COLOR_BG, size=15, weight="bold"),
        tickfont=dict(family="Inter, sans-serif", color=COLOR_BG, size=13)
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("<hr style='border: 1px solid #333; margin: 50px 0;'>", unsafe_allow_html=True)

# ==========================================
# 6. FITUR SIMULATOR KEBIJAKAN
# ==========================================
st.markdown("<div id='simulator' style='padding-top: 100px; margin-top: -60px;'></div>", unsafe_allow_html=True) 
st.markdown(f"<h2 style='text-align: center; color: {COLOR_CREAM}; margin-bottom: 20px; font-weight: 800;'>Simulator Kebijakan Berbasis Machine Learning</h2>", unsafe_allow_html=True)

@st.fragment
def simulator_section():
    st.markdown("<p style='text-align: center; margin-bottom: 40px; color: #ccc; font-size: 1.1rem;'>Pilih daerah dan atur target pendidikan untuk melihat prediksi penurunan persentase kemiskinan.</p>", unsafe_allow_html=True)
    
    _, col_sim, _ = st.columns([1, 4, 1])
    
    with col_sim:
        selected_kab = st.selectbox("Pilih Kabupaten/Kota:", df['Nama_Daerah'].tolist())
        data_kab = df[df['Nama_Daerah'] == selected_kab].iloc[0]

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("RLS Aktual", f"{data_kab['RLS']:.2f} Tahun")
        c2.metric("IPM Aktual", f"{data_kab['IPM']:.2f}")
        c3.metric("Kemiskinan Aktual", f"{data_kab['Kemiskinan']:.2f}%")
        st.markdown("<br><br>", unsafe_allow_html=True)

        target_rls = st.slider("Tetapkan Target Rata-rata Lama Sekolah (Tahun)", 
                               min_value=float(df['RLS'].min()), max_value=15.0, value=float(data_kab['RLS']))

        prediksi_awal = model.predict([[data_kab['RLS']]])[0]
        prediksi_baru = model.predict([[target_rls]])[0]

        st.markdown(f"""
            <div style='background-color: {COLOR_BROWN}; padding: 40px; border-radius: 20px; text-align: center; margin-top: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); box-sizing: border-box;'>
                <h4 style='font-family: Montserrat, sans-serif; color: {COLOR_CREAM}; margin-bottom: 15px; font-weight: 700;'>Prediksi Tingkat Kemiskinan Baru:</h4>
                <h1 style='font-family: Montserrat, sans-serif; color: white; font-size: 4.5rem; font-weight: 900; margin: 0;'>{max(0, prediksi_baru):.2f}%</h1>
                <p style='color: #e0e0e0; margin-top: 20px; font-size: 1.15rem; line-height: 1.6;'>
                    Dengan intervensi RLS menjadi <b>{target_rls:.2f} tahun</b>, estimasi penurunan kemiskinan adalah sebesar <b>{(prediksi_awal - prediksi_baru):.2f}%</b> (Ceteris Paribus).
                </p>
            </div>
        """, unsafe_allow_html=True)

simulator_section()

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align: center; margin-top: 60px; margin-bottom: 30px;">
    <a href="#beranda" target="_self" style="font-family: Montserrat, sans-serif; color: {COLOR_CREAM}; text-decoration: none; font-size: 1.1rem; font-weight: 700; border-bottom: 2px solid {COLOR_CREAM}; padding-bottom: 5px; transition: 0.3s;">&uarr; Kembali ke Atas</a>
</div>
""", unsafe_allow_html=True)