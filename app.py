import streamlit as st
import time
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Fatih Kriz ve ÇEDEP Asistanı", page_icon="🧩", layout="centered")

st.title("🧩 Fatih Kriz ve ÇEDEP Destek Paneli")
st.write("Anne, Baba ve Abla için Ortak Koordinasyon Asistanı")

# Veri dosyası adı
DATA_FILE = "cedep_kayitlari.csv"

# Kayıtları tutmak için fonksiyon
def kaydet_etkinlik(ilgilenen, etkinlik):
    simdi = datetime.now().strftime("%d-%m-%Y %H:%M")
    yeni_veri = pd.DataFrame([[simdi, ilgilenen, etkinlik]], columns=["Tarih", "Kim İlgilendi", "Etkinlik / Çalışma"])
    
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, yeni_veri], ignore_index=True)
    else:
        df = yeni_veri
    df.to_csv(DATA_FILE, index=False)

# Sekmeler
tab1, tab2, tab3 = st.tabs(["🚨 Acil Kriz Koçu", "⏱️ Ekran / Sayaç", "📋 Günlük ÇEDEP Takibi"])

with tab1:
    st.header("Acil Kriz Anı Ne Yapmalı?")
    kriz_turu = st.selectbox("Şu an hangi kriz yaşanıyor?", ["-- Seçiniz --", "Telefonu vermiyor / Kapatınca ağlıyor", "İsteği anında yapılmadı, kendini yere attı"])
    
    if kriz_turu == "Telefonu vermiyor / Kapatınca ağlıyor":
        st.error("🛑 ACİL UYGULAMA ADIMI:")
        st.markdown("""
        1. **Göz Hizasına inin ve sakin bir sesle tek cümle kurun:**  
           > *"Süre bitti. Biliyorum üzgünsün ama telefon kapalı."*
        2. **Suçu size değil, saate atın:**  
           > *"Ben kapatmadım, saat çaldı, telefonun süresi bitti."*
        3. **Ortamı değiştirin (Duyusal Reset):**  
           Dikkatini dağıtmak için hemen balkona veya pencere önüne götürüp dışarıdaki araçlara bakın.
        """)
    elif kriz_turu == "İsteği anında yapılmadı, kendini yere attı":
        st.error("🛑 ACİL UYGULAMA ADIMI:")
        st.markdown("""
        1. **Pazarlık Etmeyin / Uzun Açıklama Yapmayın:** Yerde ağlarken mantık yürütülmez.
        2. **Ortak Cümleyi Söyleyin:**  
           > *"Ağlayabilirsin, buradayım ama istediğin şu an olmuyor."*
        3. **Sakinleşme Alanı:** Dikkatini farklı bir nesneye yöneltin.
        """)

with tab2:
    st.header("Ekran Süresi Sayaç Paneli")
    sure = st.slider("Dakika Seçin", 1, 30, 10)
    if st.button("Süreyi Başlat"):
        with st.empty():
            for s in range(sure * 60, 0, -1):
                dakika, saniye = divmod(s, 60)
                st.subheader(f"Kalan Süre: {dakika:02d}:{saniye:02d}")
                time.sleep(1)
            st.success("🔔 SÜRE BİTTİ! Şimdi telefonu kapatma zamanı.")

with tab3:
    st.header("Bugünkü ÇEDEP / Etkinlik Takibi")
    ilgilenen = st.radio("Bugün Fatih ile kim ilgilendi?", ["Anne", "Baba", "Abla (Sen)"])
    etkinlik = st.text_input("Bugün yapılan çalışma (Örn: Yönerge takibi, eşleştirme, yürüyüş):")
    
    if st.button("Kaydet"):
        if etkinlik.strip() != "":
            kaydet_etkinlik(ilgilenen, etkinlik)
            st.success(f"Harika! Kaydedildi: {ilgilenen} - {etkinlik}")
        else:
            st.warning("Lütfen yapılan çalışmayı boş bırakmayın.")
            
    st.markdown("---")
    st.subheader("📜 Geçmiş ÇEDEP Çalışmaları ve Takibi")
    
    if os.path.exists(DATA_FILE):
        df_kayitlar = pd.read_csv(DATA_FILE)
        if not df_kayitlar.empty:
            st.dataframe(df_kayitlar, use_container_width=True)
        else:
            st.info("Henüz kayıtlı bir ÇEDEP çalışması yok.")
    else:
        st.info("Henüz kayıt bulunmuyor. İlk çalışmayı yukarıdan ekleyebilirsiniz.")
