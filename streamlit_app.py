import streamlit as st
from datetime import date

st.set_page_config(page_title="Panda Geoteknik Pro Max", layout="wide")

st.title("🏗️ Panda Profesyonel Geoteknik & Şantiye Yönetimi")
tab1, tab2 = st.tabs(["📊 Detaylı Hakediş & Analiz", "📝 Günlük Rapor & Saha Gideri"])

# --- TAB 1: DETAYLI ANALİZ (HESAP MAKİNESİ) ---
with tab1:
    with st.expander("💰 Birim Fiyatlar ve Genel Giderler (TL)", expanded=False):
        f1, f2, f3, f4 = st.columns(4)
        p_beton = f1.number_input("Beton (m3)", value=2800)
        p_demir = f2.number_input("Donatı (Ton)", value=30000)
        p_halat = f3.number_input("Ankraj Halatı (m)", value=130)
        p_boru = f4.number_input("Boru/Profil (kg)", value=45)
        
        f5, f6, f7, f8 = st.columns(4)
        p_personel = f5.number_input("Günlük Maaş (Ort. TL)", value=1500)
        p_yemek = f6.number_input("Günlük Yemek (TL/Kişi)", value=250)
        p_kamp = f7.number_input("Günlük Konaklama (TL/Kişi)", value=400)
        p_yakit = f8.number_input("Mazot (Litre/TL)", value=45)

    st.subheader("🛠️ Tüm İmalat Kalemleri")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        d_duvar = st.number_input("Diyafram Duvar (m2)", value=0.0)
        f_kazik = st.number_input("Fore Kazık (m)", value=0.0)
        b_kazik = st.number_input("Boru Kazık (m)", value=0.0)
    
    with c2:
        jet_grout = st.number_input("Jet Grout (m)", value=0.0)
        enjeksiyon = st.number_input("Enjeksiyon (m)", value=0.0)
        ankraj = st.number_input("Ankraj (Toplam m)", value=0.0)
    
    with c3:
        b_kiris = st.number_input("Başlık Kirişi (m3)", value=0.0)
        strut = st.number_input("Strut / Çelik Destek (Ton)", value=0.0)
        p_beton_m2 = st.number_input("Püskürtme Beton (m2)", value=0.0)

    st.divider()
    
    st.subheader("👤 Kadro ve Süre")
    k1, k2, k3, k4 = st.columns(4)
    n_personel = k1.number_input("Toplam Personel Sayısı", value=15)
    proje_gun = k2.number_input("Proje Süresi (Gün)", value=30)
    gunluk_yakit = k3.number_input("Günlük Yakıt Tüketimi (Litre)", value=100)

    # HESAPLAMA MOTORU
    analiz_verisi = []
    
    # İmalat Hesapları
    def ekle(isim, metraj, beton, demir_halat, maliyet):
        analiz_verisi.append({"Kalem": isim, "Metraj": metraj, "Beton (m3)": beton, "Donatı/Halat/Çelik": demir_halat, "Maliyet (TL)": f"{maliyet:,.0f}"})

    toplam_imalat_maliyeti = 0

    if d_duvar > 0:
        m = (d_duvar*0.8*p_beton) + ((d_duvar*0.8*120)/1000*p_demir)
        ekle("Diyafram Duvar", f"{d_duvar} m2", d_duvar*0.8, f"{(d_duvar*0.8*120)/1000:.2f} Ton", m)
        toplam_imalat_maliyeti += m
    if f_kazik > 0:
        m = (f_kazik*0.5*p_beton) + ((f_kazik*0.5*100)/1000*p_demir)
        ekle("Fore Kazık", f"{f_kazik} m", f_kazik*0.5, f"{(f_kazik*0.5*100)/1000:.2f} Ton", m)
        toplam_imalat_maliyeti += m
    if jet_grout > 0:
        m = jet_grout * 600 # Ortalama çimento/m maliyeti varsayımı
        ekle("Jet Grout", f"{jet_grout} m", "-", "Çimento Bazlı", m)
        toplam_imalat_maliyeti += m
    if ankraj > 0:
        m = (ankraj*0.05*p_beton) + (ankraj*4*p_halat)
        ekle("Ankraj", f"{ankraj} m", ankraj*0.05, f"{ankraj*4:.0f} m Halat", m)
        toplam_imalat_maliyeti += m
    if strut > 0:
        m = strut * 1000 * p_boru
        ekle("Strut", f"{strut} Ton", "-", f"{strut} Ton Profil", m)
        toplam_imalat_maliyeti += m
    if p_beton_m2 > 0:
        m = (p_beton_m2*0.1*p_beton) + (p_beton_m2*1.1*450)
        ekle("Püskürtme Beton", f"{p_beton_m2} m2", p_beton_m2*0.1, f"{p_beton_m2*1.1:.1f} m2 Hasır", m)
        toplam_imalat_maliyeti += m

    # Genel Gider Hesapları
    personel_toplam = n_personel * p_personel * proje_gun
    yemek_toplam = n_personel * (p_yemek * 3) * proje_gun
    kamp_toplam = n_personel * p_kamp * proje_gun
    yakit_toplam = gunluk_yakit * p_yakit * proje_gun
    genel_gider_toplam = personel_toplam + yemek_toplam + kamp_toplam + yakit_toplam

    ekle("👤 Personel & Maaş", f"{n_personel} Kişi", "-", f"{proje_gun} Gün", personel_toplam)
    ekle("🍲 Yemek & Konaklama", "Kamp Gideri", "-", "3 Öğün + Yatak", yemek_toplam + kamp_toplam)
    ekle("⛽ Yakıt Gideri", f"{gunluk_yakit} L/Gün", "-", f"Toplam {gunluk_yakit*proje_gun} L", yakit_toplam)

    st.subheader("📋 Kapsamlı Hakediş Tablosu")
    st.table(analiz_verisi)
    
    st.error(f"### PROJE GENEL TOPLAM MALİYETİ: {toplam_imalat_maliyeti + genel_gider_toplam:,.2f} TL")

# --- TAB 2: GÜNLÜK RAPOR ---
with tab2:
    st.header("📝 Günlük Saha Kayıtları")
    secilenler = st.multiselect("Bugün yapılan işleri seçin:", ["Diyafram Duvar", "Fore Kazık", "Jet Grout", "Ankraj", "Enjeksiyon", "Boru Kazık", "Başlık Kirişi", "Strut", "Püskürtme Beton"])
    
    if secilenler:
        rapor_data = []
        for kalem in secilenler:
            st.markdown(f"#### {kalem}")
            r1, r2, r3, r4 = st.columns(4)
            metraj = r1.number_input(f"Metraj", key=f"r_m_{kalem}")
            beton = r2.number_input(f"Beton (m3)", key=f"r_b_{kalem}")
            demir = r3.number_input(f"Donatı/Halat/Çelik", key=f"r_d_{kalem}")
            notu = r4.text_input(f"Not", key=f"r_n_{kalem}")
            rapor_data.append({"İmalat": kalem, "Metraj": metraj, "Beton": beton, "Donatı/Halat/Çelik": demir, "Not": notu})
        
        if st.button("🚀 Raporu Kapat ve Onayla"):
            st.success("Günlük Rapor Hazırlandı.")
            st.table(rapor_data)
