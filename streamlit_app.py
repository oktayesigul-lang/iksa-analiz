import streamlit as st
from datetime import date

# Sayfa Ayarları
st.set_page_config(page_title="Panda Geoteknik Global", layout="wide")

# --- DİL VE PARA BİRİMİ SEÇİMİ ---
st.sidebar.title("🌍 Ayarlar / Настройки")
dil = st.sidebar.radio("Dil Seçimi / Выбор языка", ["Türkçe", "Русский"])
para_birimi = st.sidebar.radio("Para Birimi / Валюта", ["TL", "RUB"])
kur = st.sidebar.number_input("1 TL kaç Ruble? / Курс TL к Рублю", value=2.85)

# Metin Sözlüğü
T = {
    "Türkçe": {
        "baslik": "🏗️ Panda Profesyonel Geoteknik & Şantiye Yönetimi",
        "tab1": "📊 Detaylı Hakediş & Analiz",
        "tab2": "📝 Günlük Rapor & Saha Gideri",
        "birim_fiyat": "💰 Birim Fiyatlar ve Genel Giderler",
        "imalat_kalem": "🛠️ Tüm İmalat Kalemleri",
        "kadro": "👤 Kadro ve Süre",
        "toplam": "PROJE GENEL TOPLAM MALİYETİ",
        "kalemler": ["Diyafram Duvar", "Fore Kazık", "Boru Kazık", "Jet Grout", "Enjeksiyon", "Ankraj", "Başlık Kirişi", "Strut", "Püskürtme Beton", "Personel & Maaş", "Yemek & Konaklama", "Yakıt Gideri"],
        "tablo_baslik": ["Kalem", "Metraj", "Beton (m3)", "Donatı/Halat/Çelik", "Maliyet"],
        "günlük": "📝 Günlük Saha Kayıtları",
        "rapor_buton": "🚀 Raporu Kapat ve Onayla"
    },
    "Русский": {
        "baslik": "🏗️ Panda Профессиональное Геотехническое Управление",
        "tab1": "📊 Детальный Расчет и Анализ",
        "tab2": "📝 Ежедневный Отчет и Расходы",
        "birim_fiyat": "💰 Единичные Расценки и Расходы",
        "imalat_kalem": "🛠️ Все Виды Работ",
        "kadro": "👤 Кадры и Сроки",
        "toplam": "ОБЩАЯ СТОИМОСТЬ ПРОЕКТА",
        "kalemler": ["Диафрагменная стена", "Буронабивные сваи", "Трубчатые сваи", "Jet Grout", "Инъектирование", "Анкер", "Обвязочная балка", "Распорка", "Торкрет бетон", "Персонал и З/П", "Питание и Жилье", "Расход Топлива"],
        "tablo_baslik": ["Вид работ", "Объем", "Бетон (м3)", "Арматура/Канат/Сталь", "Стоимость"],
        "günlük": "📝 Ежедневные Полевые Записи",
        "rapor_buton": "🚀 Закрыть и Подтвердить Отчет"
    }
}

L = T[dil]
katsayi = kur if para_birimi == "RUB" else 1.0

# --- ANA PANEL ---
st.title(L["baslik"])
tab1, tab2 = st.tabs([L["tab1"], L["tab2"]])

with tab1:
    with st.expander(f"{L['birim_fiyat']} ({para_birimi})", expanded=False):
        f1, f2, f3 = st.columns(3)
        p_beton = f1.number_input(f"Beton / Бетон (m3)", value=2800.0) * katsayi
        p_demir = f2.number_input(f"Donatı / Арматура (Ton)", value=30000.0) * katsayi
        p_personel = f3.number_input(f"Maaş / Зарплата (Gülük/Ежедневно)", value=1500.0) * katsayi

    st.subheader(L["imalat_kalem"])
    c1, c2, c3 = st.columns(3)
    d_duvar = c1.number_input(f"{L['kalemler'][0]} (m2)", value=0.0)
    f_kazik = c1.number_input(f"{L['kalemler'][1]} (m)", value=0.0)
    ankraj = c2.number_input(f"{L['kalemler'][5]} (m)", value=0.0)
    n_pers = c3.number_input(f"{L['kalemler'][9]} (Kişi/Чел)", value=15)
    proje_gun = c3.number_input("Süre / Срок (Gün/Дней)", value=30)

    # Hesaplama ve Tablo
    analiz = []
    toplam = 0

    if d_duvar > 0:
        cost = (d_duvar*0.8*p_beton) + ((d_duvar*0.8*120)/1000*p_demir)
        analiz.append({L["tablo_baslik"][0]: L["kalemler"][0], L["tablo_baslik"][1]: f"{d_duvar} m2", L["tablo_baslik"][2]: d_duvar*0.8, L["tablo_baslik"][3]: f"{(d_duvar*0.8*120)/1000:.2f} T", L["tablo_baslik"][4]: f"{cost:,.0f} {para_birimi}"})
        toplam += cost
    
    # Personel Gideri
    pers_cost = n_pers * p_personel * proje_gun
    analiz.append({L["tablo_baslik"][0]: L["kalemler"][9], L["tablo_baslik"][1]: f"{n_pers} Pers.", L["tablo_baslik"][2]: "-", L["tablo_baslik"][3]: f"{proje_gun} Gün", L["tablo_baslik"][4]: f"{pers_cost:,.0f} {para_birimi}"})
    toplam += pers_cost

    st.subheader(f"📋 {L['tab1']}")
    st.table(analiz)
    st.error(f"### {L['toplam']}: {toplam:,.2f} {para_birimi}")

with tab2:
    st.header(L["günlük"])
    # Dinamik Rapor Alanı (Dil desteğiyle)
    secilenler = st.multiselect("✅", L["kalemler"][:9])
    if secilenler:
        for s in secilenler:
            st.write(f"**{s}**")
            # Giriş kutuları buraya...
        if st.button(L["rapor_buton"]):
            st.success("OK!")
