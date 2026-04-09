import streamlit as st
from datetime import date

st.set_page_config(page_title="Panda Geoteknik Pro", layout="wide")

# ANA BAŞLIK
st.title("🏗️ Panda Profesyonel Geoteknik & Temel Mühendisliği Paneli")
tab1, tab2 = st.tabs(["📊 Detaylı Analiz & Metraj", "📝 Günlük Rapor Modülü"])

# --- TAB 1: DETAYLI ANALİZ (HESAP MAKİNESİ) ---
with tab1:
    with st.expander("💰 Birim Fiyat Tanımlama (TL)", expanded=False):
        f1, f2, f3, f4, f5 = st.columns(5)
        p_beton = f1.number_input("Beton (m3)", value=2800)
        p_demir = f2.number_input("Donatı (Ton)", value=30000)
        p_halat = f3.number_input("Halat (m)", value=130)
        p_boru = f4.number_input("Boru/Profil (kg)", value=45)
        p_hasir = f5.number_input("Hasır Çelik (m2)", value=450)

    st.subheader("🛠️ Proje İmalat Parametreleri")
    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        d_duvar_m2 = st.number_input("Diyafram Duvar (m2)", value=0.0)
        f_kazik_m = st.number_input("Fore Kazık (m)", value=0.0)
    with col_2:
        jet_grout_m = st.number_input("Jet Grout (m)", value=0.0)
        ankraj_m = st.number_input("Ankraj (Toplam m)", value=0.0)
    with col_3:
        b_kiris_m3 = st.number_input("Başlık Kirişi (m3)", value=0.0)
        p_beton_m2 = st.number_input("Püskürtme Beton (m2)", value=0.0)

    analiz_listesi = []
    if d_duvar_m2 > 0:
        v_beton = d_duvar_m2 * 0.8
        w_demir = (v_beton * 120) / 1000
        analiz_listesi.append({"Kalem": "Diyafram Duvar", "Metraj": f"{d_duvar_m2} m2", "Beton (m3)": v_beton, "Donatı/Halat/Çelik": f"{w_demir:.2f} Ton", "Maliyet": f"{(v_beton*p_beton)+(w_demir*p_demir):,.0f}"})
    if f_kazik_m > 0:
        v_beton = f_kazik_m * 0.5
        w_demir = (v_beton * 100) / 1000
        analiz_listesi.append({"Kalem": "Fore Kazık", "Metraj": f"{f_kazik_m} m", "Beton (m3)": v_beton, "Donatı/Halat/Çelik": f"{w_demir:.2f} Ton", "Maliyet": f"{(v_beton*p_beton)+(w_demir*p_demir):,.0f}"})
    
    if analiz_listesi:
        st.subheader("📋 Detaylı Analiz Tablosu")
        st.table(analiz_listesi)

# --- TAB 2: GÜNLÜK RAPOR MODÜLÜ ---
with tab2:
    st.header("📝 Günlük Saha Raporu")
    
    # 1. Aşama: Şantiye Kimliği
    with st.expander("🏢 Proje ve Hava Durumu Bilgisi", expanded=True):
        c1, c2, c3 = st.columns(3)
        proje_adi = c1.text_input("Proje Adı", value="Moskova Şantiyesi")
        tarih = c2.date_input("Rapor Tarihi", date.today())
        hava = c3.selectbox("Hava Durumu", ["Güneşli", "Yağmurlu", "Karlı", "Sert Rüzgarlı"])

    st.divider()

    # 2. Aşama: Parametre Seçimi
    st.subheader("✅ Bugün Yapılan İmalatları Seçin")
    secilenler = st.multiselect(
        "Listeyi Düzenle:", 
        ["Diyafram Duvar", "Fore Kazık", "Jet Grout", "Ankraj", "Enjeksiyon", "Boru Kazık", "Başlık Kirişi", "Strut", "Püskürtme Beton"],
        default=[]
    )

    # 3. Aşama: Dinamik Veri Girişi
    if secilenler:
        st.write("---")
        st.subheader("📊 İmalat Detayları")
        
        gunluk_veriler = []
        
        for kalem in secilenler:
            st.markdown(f"#### 📍 {kalem}")
            r1, r2, r3, r4 = st.columns(4)
            
            metraj = r1.number_input(f"{kalem} Metrajı", min_value=0.0, key=f"m_{kalem}")
            
            # Kaleme göre özel birimler
            if kalem in ["Diyafram Duvar", "Fore Kazık", "Başlık Kirişi"]:
                beton = r2.number_input(f"Beton (m3) - {kalem}", min_value=0.0, key=f"b_{kalem}")
                donati = r3.number_input(f"Donatı (Ton) - {kalem}", min_value=0.0, key=f"d_{kalem}")
                notu = r4.text_input(f"Notlar - {kalem}", key=f"n_{kalem}")
                gunluk_veriler.append({"İmalat": kalem, "Metraj": metraj, "Beton": beton, "Donatı/Halat/Boru": donati, "Not": notu})
            
            elif kalem == "Ankraj":
                enj = r2.number_input("Enjeksiyon (m3)", min_value=0.0, key="b_ank")
                halat = r3.number_input("Halat (m)", min_value=0.0, key="d_ank")
                notu = r4.text_input("Notlar - Ankraj", key="n_ank")
                gunluk_veriler.append({"İmalat": kalem, "Metraj": metraj, "Beton": enj, "Donatı/Halat/Boru": halat, "Not": notu})
            
            elif kalem == "Boru Kazık":
                boru = r2.number_input("Boru Ağırlığı (kg)", min_value=0.0, key="d_boru")
                notu = r4.text_input("Notlar - Boru Kazık", key="n_boru")
                gunluk_veriler.append({"İmalat": kalem, "Metraj": metraj, "Beton": "-", "Donatı/Halat/Boru": boru, "Not": notu})
            
            else: # Genel Giriş
                notu = r4.text_input(f"Notlar - {kalem}", key=f"n_{kalem}")
                gunluk_veriler.append({"İmalat": kalem, "Metraj": metraj, "Beton": "-", "Donatı/Halat/Boru": "-", "Not": notu})

        # 4. Aşama: Raporu Onaylama ve Tablo
        st.divider()
        if st.button("🚀 Raporu Kaydet ve Özetle"):
            st.success(f"{proje_adi} - {tarih} Tarihli Rapor Hazır!")
            st.table(gunluk_veriler)
            st.info("Bu özet tabloyu kopyalayıp Excel veya WhatsApp grubuna yapıştırabilirsiniz.")
    else:
        st.warning("Lütfen bugün yapılan imalatları listeden seçin.")

# Footer
st.markdown("---")
st.caption("Panda's Engineering & Vibe Station - 2026")
