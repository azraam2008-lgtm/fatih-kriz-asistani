import streamlit as st
import pandas as pd
import os
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="Fatih Kriz ve ÇEDEP Asistanı", page_icon="🧩", layout="centered")

st.title("🧩 Fatih Kriz ve ÇEDEP Destek Paneli")
st.write("Anne, Baba ve Abla için Ortak Koordinasyon Asistanı")

# Veri Dosyaları
CEDEP_FILE = "cedep_kayitlari.csv"
 EKRAN_FILE = "ekran_kayitlari.csv"

# ÇEDEP Kayıt Fonksiyonu
def kaydet_cedep(ilgilenen, etkinlik):
    simdi = datetime.now().strftime("%d-%m-%Y %H:%M")
    yeni_veri = pd.DataFrame([[simdi, ilgilenen, etkinlik]], columns=["Tarih", "Kim İlgilendi", "Etkinlik / Çalışma"])
    if os.path.exists(CEDEP_FILE):
        df = pd.read_csv(CEDEP_FILE)
        df = pd.concat([df, yeni_veri], ignore_index=True)
    else:
        df = yeni_veri
    df.to_csv(CEDEP_FILE, index=False)

# Ekran Süresi Kayıt Fonksiyonu
def kaydet_ekran(sure_dk):
    simdi = datetime.now().strftime("%d-%m-%Y %H:%M")
    bugun_tarih = datetime.now().strftime("%d-%m-%Y")
    yeni_veri = pd.DataFrame([[simdi, bugun_tarih, sure_dk]], columns=["Zaman", "Tarih", "Verilen Sure (dk)"])
    if os.path.exists(EKRAN_FILE):
        df = pd.read_csv(EKRAN_FILE)
        df = pd.concat([df, yeni_veri], ignore_index=True)
    else:
        df = yeni_veri
    df.to_csv(EKRAN_FILE, index=False)

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
    sure_dk = st.slider("Dakika Seçin (Maks 60 dk)", 1, 60, 15)
    
    if st.button("Süreyi Başlat ve Kaydet"):
        kaydet_ekran(sure_dk)
        st.success(f"{sure_dk} dakika ekran süresi başarıyla kaydedildi ve sayaç başlatıldı!")

    # Arka planda çalışan ve sekme kapansa bile alarm veren JS/HTML Zamanlayıcı
    sure_saniye = sure_dk * 60
    javascript_sayac = f"""
    <div>
        <h2 id="timer-display" style="text-align: center; color: #1f77b4; font-size: 40px;">Kalan Süre: {sure_dk:02d}:00</h2>
        <div id="alarm-box" style="text-align: center;"></div>
    </div>
    
    <script>
        let totalSeconds = {sure_saniye};
        const display = document.getElementById('timer-display');
        const alarmBox = document.getElementById('alarm-box');
        
        function playAlarm() {{
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.type = 'sine';
            osc.frequency.value = 587.33;
            osc.start();
            setTimeout(() => {{ osc.stop(); }}, 2000);
        }}

        const timerInterval = setInterval(() => {{
            if (totalSeconds <= 0) {{
                clearInterval(timerInterval);
                display.innerHTML = "🚨 SÜRE BİTTİ! 🚨";
                display.style.color = "red";
                alarmBox.innerHTML = "<h3 style='color: red;'>🔔 Süre doldu! Şimdi telefonu kapatma zamanı (Suçu saate atmayı unutmayın!).</h3>";
                playAlarm();
            }} else {{
                totalSeconds--;
                let m = Math.floor(totalSeconds / 60);
                let s = totalSeconds % 60;
                display.innerHTML = "Kalan Süre: " + String(m).padStart(2, '0') + ":" + String(s).padStart(2, '0');
            }}
        }}, 1000);
    </script>
    """
    
    components.html(javascript_sayac, height=150)
    
    st.markdown("---")
    st.subheader("📊 Ekran Süresi Geçmişi ve Günlük Toplam")
    
    if os.path.exists(EKRAN_FILE):
        df_ekran = pd.read_csv(EKRAN_FILE)
        if not df_ekran.empty:
            # Bugün verilen toplam süreyi hesapla
            bugun_str = datetime.now().strftime("%d-%m-%Y")
            bugun_df = df_ekran[df_ekran["Tarih"] == bugun_str]
            toplam_bugun = bugun_df["Verilen Sure (dk)"].sum() if not bugun_df.empty else 0
            
            st.metric(label="📅 Bugün Verilen Toplam Ekran Süresi", value=f"{toplam_bugun} Dakika")
            
            st.markdown("### Tüm Ekran Süresi Geçmişi")
            st.dataframe(df_ekran, use_container_width=True)
        else:
            st.info("Henüz ekran süresi kaydı bulunmuyor.")
    else:
        st.info("Henüz ekran süresi kaydı bulunmuyor.")

with tab3:
    st.header("Bugünkü ÇEDEP / Etkinlik Takibi")
    ilgilenen = st.radio("Bugün Fatih ile kim ilgilendi?", ["Anne", "Baba", "Abla (Sen)"])
    etkinlik = st.text_input("Bugün yapılan çalışma (Örn: Yönerge takibi, eşleştirme, yürüyüş):")
    
    if st.button("Kaydet", key="cedep_kaydet"):
        if etkinlik.strip() != "":
            kaydet_cedep(ilgilenen, etkinlik)
            st.success(f"Harika! Kaydedildi: {ilgilenen} - {etkinlik}")
        else:
            st.warning("Lütfen yapılan çalışmayı boş bırakmayın.")
            
    st.markdown("---")
    st.subheader("📜 Geçmiş ÇEDEP Çalışmaları ve Takibi")
    
    if os.path.exists(CEDEP_FILE):
        df_kayitlar = pd.read_csv(CEDEP_FILE)
        if not df_kayitlar.empty:
            st.dataframe(df_kayitlar, use_container_width=True)
        else:
            st.info("Henüz kayıtlı bir ÇEDEP çalışması yok.")
    else:
        st.info("Henüz kayıt bulunmuyor. İlk çalışmayı yukarıdan ekleyebilirsiniz.")

   
