import streamlit as st
from datetime import date

st.set_page_config(page_title="Panda Geoteknik Pro", layout="wide")

st.title("🏗️ Panda Profesyonel Geoteknik & Hakediş Paneli")
tab1, tab2 = st.tabs(["📊 Detaylı Analiz & Metraj", "📝 Günlük Rapor Modülü"])

# --- TAB 1: DETAYLI ANALİZ ---
with tab1:
    with st.expander("💰 Birim Fiyatlar", expanded=False):
        f1, f2, f3, f4, f5 = st.columns(5)
        p_beton = f1.number_input("Beton (m3)", value=2800)
        p_demir = f2.number_input("Donatı (Ton)", value=30000)
        p_halat = f3.number_input("Halat (m)", value=130)
        p_boru = f4.number_input("Boru/Profil (kg)", value=45)
        p_hasir = f5.number_input("Hasır Çelik (m2)", value=450)

    st.subheader("🛠️ Proje İmalat Parametreleri")
    c1, c2, c3 = st.columns(3)
    
    # Tüm girişleri burada topluyoruz ki tabloda gözüksün
    d_duvar = c1.number_input("Diyafram Duvar (m2)", value=0.0, key="ana_d")
    f_kazik = c1.number_input("Fore Kazık (m)", value=0.0, key="ana_f")
    b_kazik = c1.number_input("Boru Kazık (m)", value=0.0, key="ana_b")
    
    jet_g = c2.number_input("Jet Grout (m)", value=0.0, key="ana_j")
    enj = c2.number_input("Enjeksiyon (m)", value=0.0, key="ana_e")
    ankraj = c2.number_input("Ankraj (Toplam m)", value=0.0, key="ana_a")
    
    b_kiris = c3.number_input("Başlık Kirişi (m3)", value=0.0, key="ana_bk")
    strut = c3.number_input("Strut / Çelik Destek (Ton)", value=0.0, key="ana_s")
    p_beton_m2 = c3.number_input("Püskürtme Beton (m2)", value=0.0, key="ana_pb")

    # TABLO HESAPLAMA MANTIĞI
    # Her satırı tek tek tanımlıyoruz ki "silinme" olmasın
    data = [
        {"Kalem": "Diyafram Duvar", "Metraj": f"{d_duvar} m2", "Beton (m3)": d_duvar*0.8, "Donatı/Halat/Çelik": f"{(d_duvar*0.8*120)/1000:.2f} Ton", "Maliyet": f"{(d_duvar*0.8*p_beton) + ((d_duvar*0.8*120)/1000*p_demir):,.0f}"},
        {"Kalem": "Fore Kazık", "Metraj": f"{f_kazik} m", "Beton (m3)": f_kazik*0.5, "Donatı/Halat/Çelik": f"{(f_kazik*0.5*100)/1000:.2f} Ton", "Maliyet": f"{(f_kazik*0.5*p_beton) + ((f_kazik*0.5*100)/1000*p_demir):,.0f}"},
        {"Kalem": "Boru Kazık", "Metraj": f"{b_kazik} m", "Beton (m3)": "-", "Donatı/Halat/Çelik": f"{b_kazik*80:.0f} kg", "Maliyet": f"{(b_kazik*80*p_boru):,.0f}"},
        {"Kalem": "Ankraj", "Metraj": f"{ankraj} m", "Beton (m3)": ankraj*0.05, "Donatı/Halat/Çelik": f"{ankraj*4:.0f} m", "Maliyet": f"{(ankraj*0.05*p_beton) + (ankraj*4*p_halat):,.0f}"},
        {"Kalem": "Başlık Kirişi", "Metraj": f"{b_kiris} m3", "Beton (m3)": b_kiris, "Donatı/Halat/Çelik": f"{(b_kiris*150)/1000:.2f} Ton", "Maliyet": f"{(b_kiris*p_beton) + ((b_kiris*150)/1000*p_demir):,.0f}"},
        {"Kalem": "Püskürtme Beton", "Metraj": f"{p_beton_m2} m2", "Beton (m3)": p_beton_m2*0.1, "Donatı/Halat/Çelik": f"{p_beton_m2*1.1:.1f} m2", "Maliyet": f"{(p_beton_m2*0.1*p_beton) + (p_beton_m2*1.1*p_hasir):,.0f}"}
    ]

    st.subheader("📋 Detaylı Metraj & Analiz Tablosu")
    st.table(data)

# --- TAB 2: GÜNLÜK RAPOR ---
with tab2:
    st.header("📝 Günlük Saha Raporu")
    secilenler = st.multiselect("Bugün yapılan işleri seçin:", ["Diyafram Duvar", "Fore Kazık", "Jet Grout", "Ankraj", "Boru Kazık", "Başlık Kirişi", "Püskürtme Beton"])
    
    if secilenler:
        rapor_data = []
        for kalem in secilenler:
            st.markdown(f"#### {kalem}")
            r1, r2, r3 = st.columns(3)
            m_giriş = r1.number_input("Günlük Metraj", key=f"g_{kalem}")
            b_giriş = r2.number_input("Beton (m3)", key=f"gb_{kalem}")
            d_giriş = r3.number_input("Donatı/Halat/Çelik", key=f"gd_{kalem}")
            rapor_data.append({"İmalat": kalem, "Metraj": m_giriş, "Beton": b_giriş, "Donatı/Halat/Çelik": d_giriş})
        
        if st.button("🚀 Raporu Onayla"):
            st.table(rapor_data)
