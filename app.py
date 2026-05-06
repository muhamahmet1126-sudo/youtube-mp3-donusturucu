import streamlit as st
import audio_downloader
import video_isleyici
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="Muhammet Media Converter", page_icon="🚀")

st.title("🚀 Muhammet Media Converter")
st.subheader("Her yerden erişilebilir, hızlı ve kolay!")

# Menü Seçenekleri
option = st.sidebar.selectbox(
    'Hangi işlemi yapmak istersin?',
    ('YouTube MP3 İndir', 'Video Dosyasını MP3\'e Çevir')
)

if option == 'YouTube MP3 İndir':
    url = st.text_input("YouTube Linkini Buraya Yapıştır:")
    if st.button("İndirmeyi Başlat"):
        if url:
            with st.spinner('Müzik indiriliyor...'):
                sonuc = audio_downloader.mp3_indir(url)
                st.success(sonuc)
        else:
            st.warning("Lütfen geçerli bir link girin!")

elif option == 'Video Dosyasını MP3\'e Çevir':
    yuklenen_dosya = st.file_uploader("Bir video dosyası seç", type=['mp4', 'mkv', 'avi'])
    if yuklenen_dosya is not None:
        if st.button("Sese Dönüştür"):
            with st.spinner('Dönüştürülüyor...'):
                # Geçici olarak dosyayı kaydet ve işle
                with open("temp_video.mp4", "wb") as f:
                    f.write(yuklenen_dosya.getbuffer())
                sonuc = video_isleyici.videoyu_sese_cevir("temp_video.mp4")
                st.success(sonuc)
                # İndirme butonu ekle
                with open("temp_video.mp3", "rb") as f:
                    st.download_button("MP3 Dosyasını İndir", f, file_name="donusturulen.mp3")