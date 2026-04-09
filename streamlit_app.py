import streamlit as st
from datetime import date

st.set_page_config(page_title="Panda Geoteknik Pro", layout="wide")

# ANA BAŞLIK
st.title("🏗️ Panda Profesyonel Geoteknik & Temel Mühendisliği Paneli")
tab1, tab2 = st.tabs(["📊 Detaylı Analiz & Metraj", "📝 Günlük Rapor Modülü"])

# --- TAB 1: DETAYLI ANALİZ ---
with tab1:
    with st.expander("💰 Birim Fiyat Tanımlama (TL)", expanded=True):
        f1, f2, f3, f4, f5 = st.columns(5)
        p_beton = f1.number_input("Beton (m3)", value=2800)
        p_demir = f2.number_input("Donatı (Ton)", value=30000)
        p_halat = f3.number_input("Halat (m)", value=130)
        p_boru = f4.number_input("Boru/Profil (kg)", value=45)
        p_hasir = f5.number_input("Hasır Çelik (m2)", value=450)

    # İMALAT KALEMLERİ GİRİŞ ALANI
    st.subheader("🛠️ Proje İmalat Parametreleri")
    
    col_1, col_2, col_3 = st.columns(3)
    
    with col_1:
        st.markdown("**Duvar & Kazık Sistemleri**")
        d_duvar_m2 = st.number_input("Diyafram Duvar (m2)", value=0.0)
        f_kazik_m = st.number_input("Fore Kazık (m)", value=0.0)
        b_kazik_m = st.number_input("Boru Kazık (m)", value=0.0)
        
    with col_2:
        st.markdown("**Zemin İyileştirme & Destek**")
        jet_grout_m = st.number_input("Jet Grout (m)", value=0.0)
        enjeksiyon_m = st.number_input("Enjeksiyon (m)", value=0.0)
        ankraj_m = st.number_input("Ankraj (Toplam m)", value=0.0)
        
    with col_3:
        st.markdown("**Üst Yapı & İksa Destek**")
        b_kiris_m3 = st.number_input("Başlık Kirişi (m3)", value=0.0)
        strut_ton = st.number_input("Strut / Çelik Destek (Ton)", value=0.0)
        p_beton_m2 = st.number_input("Püskürtme Beton (m2)", value=0.0)

    st.divider()

    # --- HESAPLAMA MANTIĞI ---
    # Not: Bu çarpanlar ortalama mühendislik değerleridir, saha bazlı güncellenebilir.
    analiz_listesi = []

    if d_duvar_m2 > 0:
        v_beton = d_duvar_m2 * 0.8 # 80cm kalınlık varsayımı
        w_demir = (v_beton * 120) / 1000
        maliyet = (v_beton * p_beton) + (w_demir * p_demir)
        analiz_listesi.append({"Kalem": "Diyafram Duvar", "Metraj": f"{d_duvar_m2} m2", "Beton (m3)": v_beton, "Donatı/Halat/Çelik": f"{w_demir:.2f} Ton", "Maliyet (TL)": f"{maliyet:,.0f}"})

    if f_kazik_m > 0:
        v_beton = f_kazik_m * 0.5 # 80'lik kazık alanı ~0.5m2
        w_demir = (v_beton * 100) / 1000
        maliyet = (v_beton * p_beton) + (w_demir * p_demir)
        analiz_listesi.append({"Kalem": "Fore Kazık", "Metraj": f"{f_kazik_m} m", "Beton (m3)": v_beton, "Donatı/Halat/Çelik": f"{w_demir:.2f} Ton", "Maliyet (TL)": f"{maliyet:,.0f}"})

    if ankraj_m > 0:
        v_enj = ankraj_m * 0.05
        w_halat = ankraj_m * 4 # 4 halatlı varsayım
        maliyet = (v_enj * p_beton) + (w_halat * p_halat)
        analiz_listesi.append({"Kalem": "Ankraj", "Metraj": f"{ankraj_m} m", "Beton (m3)": v_enj, "Donatı/Halat/Çelik": f"{w_halat:.0f} m", "Maliyet (TL)": f"{maliyet:,.0f}"})

    if b_kazik_m > 0:
        w_boru = b_kazik_m * 80 # Örnek 80kg/m boru ağırlığı
        maliyet = (w_boru * p_boru)
        analiz_listesi.append({"Kalem": "Boru Kazık", "Metraj": f"{b_kazik_m} m", "Beton (m3)": "-", "Donatı/Halat/Çelik": f"{w_boru:.0f} kg", "Maliyet (TL)": f"{maliyet:,.0f}"})

    if b_kiris_m3 > 0:
        w_demir = b_kiris_m3 * 150 / 1000
        maliyet = (b_kiris_m3 * p_beton) + (w_demir * p_demir)
        analiz_listesi.append({"Kalem": "Başlık Kirişi", "Metraj": f"{b_kiris_m3} m3", "Beton (m3)": b_kiris_m3, "Donatı/Halat/Çelik": f"{w_demir:.2f} Ton", "Maliyet (TL)": f"{maliyet:,.0f}"})

    # --- TABLO GÖSTERİMİ ---
    st.subheader("📋 Detaylı Hakediş ve Metraj Analizi")
    if analiz_listesi:
        st.table(analiz_listesi)
    else:
        st.warning("Analiz görmek için lütfen yukarıdaki imalat miktarlarını girin.")

# --- TAB 2: GÜNLÜK RAPOR ---
with tab2:
    st.header("Saha Günlük Rapor Kayıtları")
    # Dinamik raporlama için önceki mantık korunur
    s_secimi = st.multiselect("Bugün Yapılan İmalatları Seçin", ["Diyafram Duvar", "Fore Kazık", "Jet Grout", "Ankraj", "Püskürtme Beton"])
    # ... Veri giriş alanları ...
