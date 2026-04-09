import streamlit as st
from datetime import date

# Sayfa Ayarları
st.set_page_config(page_title="Panda Mühendislik Çözümleri", layout="wide")

# ANA BAŞLIK
st.title("🏗️ Panda Geoteknik & Mühendislik Paneli")
st.markdown("---")

# SEKMELERİ OLUŞTURUYORUZ (Bu satır iki ayrı sayfa gibi davranmasını sağlar)
tab1, tab2 = st.tabs(["💰 Maliyet & Metraj Hesabı", "📝 Günlük Rapor Sistemi"])

# --- SEKME 1: MALİYET VE METRAJ HESABI ---
with tab1:
    st.header("İksa Metraj & Maliyet Analizi")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Parametreler")
        L = st.number_input("Toplam Uzunluk (m)", value=100.0, key="meta_L")
        H = st.number_input("Derinlik (m)", value=20.0, key="meta_H")
        W = st.number_input("Genişlik/Çap (cm)", value=80.0, key="meta_W") / 100
        
        st.divider()
        p_beton = st.number_input("Beton m3 Fiyatı (TL)", value=2500, key="p_bet")
        p_demir = st.number_input("Demir Ton Fiyatı (TL)", value=28000, key="p_dem")

    with col2:
        # Hesaplamalar
        beton_vol = L * H * W
        demir_ton = (beton_vol * 110) / 1000
        toplam_maliyet = (beton_vol * p_beton) + (demir_ton * p_demir)
        
        st.subheader("📊 Analiz Sonuçları")
        res_c1, res_c2 = st.columns(2)
        res_c1.metric("Beton Hacmi", f"{beton_vol:,.1f} m³")
        res_c2.metric("Demir Miktarı", f"{demir_ton:,.1f} Ton")
        
        st.success(f"### Tahmini Toplam Maliyet: {toplam_maliyet:,.2f} TL")

# --- SEKME 2: DİNAMİK GÜNLÜK RAPOR SİSTEMİ ---
with tab2:
    st.header("Günlük Rapor Modülü")
    
    # Yapılandırma Alanı
    with st.expander("⚙️ Şantiye Ayarları (Yapılandırma)", expanded=True):
        santiye_adi = st.text_input("Proje Adı", value="Moskova Projesi", key="s_name")
        imalat_kalemleri = st.multiselect(
            "Takip Edilecek Kalemler",
            ["Panel Kazısı (m2)", "Beton (m3)", "Donatı (Ton)", "Ankraj (m)", "Boş Kazı (m3)"],
            default=["Panel Kazısı (m2)", "Beton (m3)"],
            key="s_items"
        )
    
    st.divider()
    
    # Günlük Veri Girişi
    st.subheader(f"📅 Rapor Tarihi: {date.today().strftime('%d/%m/%Y')}")
    
    c1, c2 = st.columns(2)
    with c1:
        hava = st.selectbox("Hava Durumu", ["Güneşli", "Yağmurlu", "Karlı", "Sert Rüzgarlı"], key="s_weather")
    with c2:
        notlar = st.text_area("Saha Notları", key="s_notes")

    st.write("---")
    st.write("#### Günlük İmalat Miktarları")
    veriler = {}
    
    # Dinamik kolonlar
    if imalat_kalemleri:
        entry_cols = st.columns(len(imalat_kalemleri))
        for i, kalem in enumerate(imalat_kalemleri):
            with entry_cols[i]:
                deger = st.number_input(f"{kalem}", min_value=0.0, step=0.1, key=f"d_val_{i}")
                veriler[kalem] = deger

    if st.button("🚀 Raporu Kaydet ve Özetle", key="s_btn"):
        st.success(f"{santiye_adi} - Günlük Rapor Hazırlandı.")
        st.table({"İmalat Kalemi": list(veriler.keys()), "Miktar": list(veriler.values())})

# Footer
st.markdown("---")
st.caption("Panda's Engineering Solutions - 2026")
