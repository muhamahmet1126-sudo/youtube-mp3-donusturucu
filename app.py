import streamlit as st

st.title("YouTube MP3 Dönüştürücü")
st.write("Sistem şu an yükleniyor, lütfen bekleyin...")

url = st.text_input("YouTube Video Linkini Buraya Yapıştırın:")
if st.button("Dönüştür"):
    st.info("İşlem başlatılıyor...")
