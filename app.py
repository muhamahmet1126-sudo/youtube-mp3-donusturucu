import streamlit as st
from audio_downloader import download_audio
import os

st.title("YouTube MP3 Dönüştürücü")

url = st.text_input("YouTube Video Linkini Yapıştır:")

if st.button("Dönüştür"):
    if url:
        with st.spinner("Müzik indiriliyor ve dönüştürülüyor... Lütfen bekleyin."):
            try:
                # İndirme işlemini başlat
                file_path = download_audio(url)
                
                if os.path.exists(file_path):
                    with open(file_path, "rb") as file:
                        st.success("Dönüştürme Başarılı!")
                        st.download_button(
                            label="MP3 Dosyasını İndir",
                            data=file,
                            file_name=os.path.basename(file_path),
                            mime="audio/mpeg"
                        )
                else:
                    st.error("Dosya oluşturulamadı.")
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen bir URL girin.")
