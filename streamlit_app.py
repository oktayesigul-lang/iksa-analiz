import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="İksa Metraj & Maliyet", layout="wide")

# Dil Seçeneği
dil = st.sidebar.radio("Dil / Язык", ["Türkçe", "Русский"])

# Metin Tanımlamaları
texts = {
    "Türkçe": {
        "baslik": "🏗️ İksa Sistemleri Metraj & Maliyet Analizi",
        "alt_baslik": "Proje parametrelerini girerek anlık maliyet tahmini alabilirsiniz.",
        "parametreler": "Proje Parametreleri",
        "birim_fiyatlar": "Birim Fiyatlar (TL)",
        "iksa_tipi": "İksa Tipi",
        "uzunluk": "Toplam İksa Uzunluğu (m)",
        "derinlik": "İksa Derinliği (m)",
        "genislik": "Genişlik/Çap (cm)",
        "ankraj": "Ankraj Var mı?",
        "ankraj_boyu": "Ortalama Ankraj Boyu (m)",
        "ankraj_araligi": "Yatay Ankraj Aralığı (m)",
        "hesaplanan": "📊 Hesaplanan Metrajlar",
        "maliyet_analizi": "💰 Maliyet Analizi",
        "toplam": "Tahmini Toplam Proje Maliyeti",
        "kalemler": ["Beton", "Demir", "Kazı", "Ankraj (İşçilik dahil)"]
    },
    "Русский": {
        "baslik": "🏗️ Расчет объемов и стоимости ограждения котлована",
        "alt_baslik": "Введите параметры проекта для моментальной оценки стоимости.",
        "parametreler": "Параметры проекта",
        "birim_fiyatlar": "Цена за единицу (TL)",
        "iksa_tipi": "Тип ограждения",
        "uzunluk": "Общая длина (м)",
        "derinlik": "Глубина (м)",
        "genislik": "Ширина/Диаметр (см)",
        "ankraj": "Наличие анкеров?",
        "ankraj_boyu": "Средняя длина анкера (м)",
        "ankraj_araligi": "Горизонтальный шаг (м)",
        "hesaplanan": "📊 Расчетные объемы",
        "maliyet_analizi": "💰 Анализ стоимости",
        "toplam": "Ориентировочная общая стоимость",
        "kalemler": ["Бетон", "Арматура", "Выемка грунта", "Анкеры (вкл. работы)"]
    }
}

t = texts[dil]

# --- UI TASARIMI ---
st.title(t["baslik"])
st.info(t["alt_baslik"])

# Sol Menü - Girişler
st.sidebar.header(t["parametreler"])
iksa_tipi = st.sidebar.selectbox(t["iksa_tipi"], ["Diyafram Duvar / Грейфер", "Fore Kazık / БНС"])
L = st.sidebar.number_input(t["uzunluk"], value=100.0)
H = st.sidebar.number_input(t["derinlik"], value=20.0)
W = st.sidebar.number_input(t["genislik"], value=80.0) / 100

ankraj_var = st.sidebar.checkbox(t["ankraj"], value=True)
ankraj_L = 0
ankraj_adet = 0
if ankraj_var:
    ankraj_L = st.sidebar.number_input(t["ankraj_boyu"], value=15.0)
    ankraj_sira = st.sidebar.slider("Sıra Sayısı / Кол-во рядов", 1, 5, 2)
    ankraj_adim = st.sidebar.number_input(t["ankraj_araligi"], value=1.5)
    ankraj_adet = (L / ankraj_adim) * ankraj_sira

# Birim Fiyatlar
st.sidebar.header(t["birim_fiyatlar"])
p_beton = st.sidebar.number_input(f"{t['kalemler'][0]} (m3)", value=2500)
p_demir = st.sidebar.number_input(f"{t['kalemler'][1]} (Ton)", value=28000)
p_kazi = st.sidebar.number_input(f"{t['kalemler'][2]} (m3)", value=150)
p_ankraj = st.sidebar.number_input(f"{t['kalemler'][3]} (m)", value=850)

# --- HESAPLAMALAR ---
beton_vol = L * H * W
demir_ton = (beton_vol * 110) / 1000 
kazi_vol = beton_vol * 1.05 
ankraj_toplam_m = ankraj_adet * ankraj_L

c_beton = beton_vol * p_beton
c_demir = demir_ton * p_demir
c_kazi = kazi_vol * p_kazi
c_ankraj = ankraj_toplam_m * p_ankraj
genel_toplam = c_beton + c_demir + c_kazi + c_ankraj

# --- SONUÇLAR ---
st.header(t["hesaplanan"])
col1, col2, col3, col4 = st.columns(4)
col1.metric(t["kalemler"][0], f"{beton_vol:,.1f} m³")
col2.metric(t["kalemler"][1], f"{demir_ton:,.1f} Ton")
col3.metric(t["kalemler"][2], f"{kazi_vol:,.1f} m³")
col4.metric("Ankraj", f"{ankraj_toplam_m:,.0f} m")

st.header(t["maliyet_analizi"])
data = {
    "Kalem / Статья": t["kalemler"],
    "Maliyet / Стоимость (TL)": [f"{c_beton:,.0f}", f"{c_demir:,.0f}", f"{c_kazi:,.0f}", f"{c_ankraj:,.0f}"]
}
st.table(data)

st.success(f"### {t['toplam']}: {genel_toplam:,.2f} TL")

# Footer
st.markdown("---")
st.caption("Panda's Engineering Solutions - 2026")
