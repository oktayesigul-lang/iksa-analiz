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
demir_ton = (beton_vol * 110) / 1000 # 110kg/m3 varsayılan
kazi_vol = beton_vol * 1.05 # %5 fire
ankraj_toplam_m = ankraj_adet * ank
