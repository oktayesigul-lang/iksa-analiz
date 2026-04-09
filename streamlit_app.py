import streamlit as st
from datetime import date

st.set_page_config(page_title="Panda Pro Geoteknik", layout="wide")

st.title("🏗️ Panda Profesyonel Geoteknik Analiz & Hakediş")
tab1, tab2 = st.tabs(["📊 Detaylı Metraj & Analiz", "📝 Dinamik Günlük Rapor"])

# --- TAB 1: DETAYLI METRAJ ANALİZİ ---
with tab1:
    st.header("Birim Bazlı İmalat Analizi")
    
    with st.expander("📌 Birim Fiyat Tanımlamaları", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        p_beton = c1.number_input("Beton (m3/TL)", value=2800)
        p_demir = c2.number_input("Donatı (Ton/TL)", value=30000)
        p_halat = c3.number_input("Halat (m/TL)", value=120) # Ankraj halatı birim fiyatı
        p_hasir = c4.number_input("Hasır Çelik (m2/TL)", value=450)

    # 1. PANEL / KAZIK ANALİZİ
    st.subheader("1. İksa Duvarı (Panel veya Kazık)")
    col_p1, col_p2, col_p3 = st.columns(3)
    L = col_p1.number_input("Toplam Uzunluk (m)", value=100.0)
    H = col_p2.number_input("Derinlik (m)", value=20.0)
    W = col_p3.number_input("Genişlik/Çap (cm)", value=80.0) / 100

    beton_hacmi = L * H * W
    donati_ton = (beton_hacmi * 120) / 1000 # 120kg/m3 varsayılan
    
    # 2. ANKRAJ ANALİZİ
    st.subheader("2. Öngermeli Ankraj")
    col_a1, col_a2, col_a3 = st.columns(3)
    ank_adet = col_a1.number_input("Toplam Ankraj Adedi", value=150)
    ank_boy = col_a2.number_input("Ortalama Ankraj Boyu (m)", value=18.0)
    halat_sayisi = col_a3.slider("Ankraj Başına Halat Sayısı", 1, 6, 4)
    
    toplam_halat_m = ank_adet * ank_boy * halat_sayisi
    ank_enjeksiyon_m3 = (ank_adet * ank_boy * 0.05) # Yaklaşık enjeksiyon hacmi

    # 3. PÜSKÜRTME BETON (SHOTCRETE)
    st.subheader("3. Yüzey Kaplama (Püskürtme Beton)")
    col_s1, col_s2 = st.columns(2)
    shot_alan = col_s1.number_input("Kaplama Alanı (m2)", value=L*H)
    shot_kalinlik = col_s2.number_input("Kalınlık (cm)", value=10.0) / 100
    
    shot_beton_m3 = shot_alan * shot_kalinlik
    hasir_m2 = shot_alan * 1.1 # %10 bindirme payı

    st.divider()
    
    # --- ANALİZ TABLOSU ---
    st.subheader("📋 Detaylı Metraj ve Maliyet Tablosu")
    
    ana_veriler = [
        {"İmalat Kalemi": "İksa Duvarı", "Metraj": f"{L*H:.2f} m2", "Beton (m3)": f"{beton_hacmi:.1f}", "Donatı/Halat": f"{donati_ton:.2f} Ton", "Maliyet (TL)": f"{(beton_hacmi*p_beton)+(donati_ton*p_demir):,.0f}"},
        {"İmalat Kalemi": "Ankraj", "Metraj": f"{ank_adet} Adet", "Beton (m3)": f"{ank_enjeksiyon_m3:.1f}", "Donatı/Halat": f"{toplam_halat_m:.0f} m", "Maliyet (TL)": f"{(toplam_halat_m*p_halat):,.0f}"},
        {"İmalat Kalemi": "Püskürtme Beton", "Metraj": f"{shot_alan:.2f} m2", "Beton (m3)": f"{shot_beton_m3:.1f}", "Donatı/Halat": f"{hasir_m2:.1f} m2", "Maliyet (TL)": f"{(shot_beton_m3*p_beton)+(hasir_m2*p_hasir):,.0f}"}
    ]
    
    st.table(ana_veriler)

# --- TAB 2: GÜNLÜK RAPOR ---
with tab2:
    st.header("Saha Günlük Rapor")
    # (Bu kısım aynı mantıkla korunabilir, verileri yukarıdaki analizlerle bağlayabiliriz)
    st.info("Yapılandırma sekmesinden imalat kalemlerini seçip günlük giriş yapabilirsiniz.")
