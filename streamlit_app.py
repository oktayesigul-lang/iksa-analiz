import streamlit as st
from datetime import date

st.set_page_config(page_title="Panda Geoteknik Pro", layout="wide")

st.title("🏗️ Panda Profesyonel Geoteknik & Şantiye Yönetimi")
tab1, tab2 = st.tabs(["📊 Detaylı Hakediş & Analiz", "📝 Günlük Rapor & Kamp Gideri"])

# --- TAB 1: DETAYLI ANALİZ (MALİYET HESABI) ---
with tab1:
    with st.expander("💰 Birim Fiyat ve Genel Gider Tanımları", expanded=False):
        f1, f2, f3 = st.columns(3)
        p_beton = f1.number_input("Beton (m3/TL)", value=2800)
        p_demir = f2.number_input("Donatı (Ton/TL)", value=30000)
        p_personel = f3.number_input("Günlük Personel Maliyeti (Ort. TL/Kişi)", value=1500, help="Maaş + Sigorta + Diğer")
        
        f4, f5 = st.columns(2)
        p_yemek = f4.number_input("Günlük Yemek Maliyeti (TL/Öğün-Kişi)", value=250)
        p_konaklama = f5.number_input("Günlük Kamp/Konaklama Gideri (TL/Kişi)", value=400)

    st.subheader("🛠️ İmalat ve Kadro Parametreleri")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("**İmalat Miktarları**")
        d_duvar = st.number_input("Diyafram Duvar (m2)", value=0.0)
        f_kazik = st.number_input("Fore Kazık (m)", value=0.0)
        ankraj = st.number_input("Ankraj (Toplam m)", value=0.0)
    
    with c2:
        st.markdown("**Personel Sayıları**")
        n_muhendis = st.number_input("Mühendis Sayısı", value=2)
        n_operator = st.number_input("Operatör / Formeni", value=4)
        n_isci = st.number_input("Düz İşçi Sayısı", value=10)
    
    with c3:
        st.markdown("**Süre Bilgisi**")
        proje_sure = st.number_input("Tahmini Proje Süresi (Gün)", value=30)

    # HESAPLAMALAR
    toplam_personel = n_muhendis + n_operator + n_isci
    toplam_personel_maliyeti = toplam_personel * p_personel * proje_sure
    toplam_yemek_maliyeti = toplam_personel * (p_yemek * 3) * proje_sure # 3 öğün
    toplam_konaklama_maliyeti = toplam_personel * p_konaklama * proje_sure
    genel_giderler = toplam_personel_maliyeti + toplam_yemek_maliyeti + toplam_konaklama_maliyeti

    # TABLO VERİSİ
    data = [
        {"Kalem": "Diyafram Duvar", "Metraj": f"{d_duvar} m2", "Malzeme Analizi": f"Beton: {d_duvar*0.8:.1f} m3", "Maliyet (TL)": f"{(d_duvar*0.8*p_beton) + ((d_duvar*0.8*120)/1000*p_demir):,.0f}"},
        {"Kalem": "Fore Kazık", "Metraj": f"{f_kazik} m", "Malzeme Analizi": f"Beton: {f_kazik*0.5:.1f} m3", "Maliyet (TL)": f"{(f_kazik*0.5*p_beton) + ((f_kazik*0.5*100)/1000*p_demir):,.0f}"},
        {"Kalem": "Ankraj", "Metraj": f"{ankraj} m", "Malzeme Analizi": f"Halat: {ankraj*4:.0f} m", "Maliyet (TL)": f"{(ankraj*0.05*p_beton) + (ankraj*4*p_halat if 'p_halat' in locals() else 0):,.0f}"},
        {"Kalem": "👤 Personel Maaş", "Metraj": f"{toplam_personel} Kişi", "Malzeme Analizi": f"{proje_sure} Gün", "Maliyet (TL)": f"{toplam_personel_maliyeti:,.0f}"},
        {"Kalem": "🍲 Yemek & Konaklama", "Metraj": f"{toplam_personel} Kişi", "Malzeme Analizi": "3 Öğün + Kamp", "Maliyet (TL)": f"{toplam_yemek_maliyeti + toplam_konaklama_maliyeti:,.0f}"}
    ]

    st.subheader("📋 Kapsamlı Maliyet Analizi (İmalat + Genel Giderler)")
    st.table(data)
    
    st.error(f"### Proje Genel Toplamı: {genel_giderler + (d_duvar*0.8*p_beton):,.2f} TL")

# --- TAB 2: GÜNLÜK RAPOR ---
with tab2:
    st.header("📝 Günlük Saha Raporu")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        secilen_is = st.multiselect("Bugün yapılan imalatlar:", ["Diyafram Duvar", "Fore Kazık", "Ankraj"])
    with col_r2:
        mevcut_personel = st.number_input("Bugün Sahadaki Toplam Personel", value=toplam_personel)

    if secilen_is:
        rapor_list = []
        for is_adi in secilen_is:
            st.write(f"**{is_adi} Detayı**")
            m, b, d = st.columns(3)
            metraj = m.number_input(f"Metraj - {is_adi}", key=f"r_m_{is_adi}")
            beton = b.number_input(f"Beton - {is_adi}", key=f"r_b_{is_adi}")
            notlar = d.text_input(f"Saha Notu - {is_adi}", key=f"r_n_{is_adi}")
            rapor_list.append({"İmalat": is_adi, "Metraj": metraj, "Beton": beton, "Not": notlar})
        
        if st.button("🚀 Günlük Raporu Kapat"):
            st.success("Rapor Kaydedildi.")
            st.table(rapor_list)
            st.write(f"💡 Bugün {mevcut_personel} personelin yemek ve konaklama maliyeti: {mevcut_personel * (p_yemek*3 + p_konaklama):,.0f} TL")
