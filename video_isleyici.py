from moviepy import VideoFileClip
import os

def videoyu_sese_cevir(video_yolu):
    try:
        # Çıkış dosya adını oluştur (video.mp4 -> video.mp3)
        dosya_adi, uzanti = os.path.splitext(video_yolu)
        cikis_adi = f"{dosya_adi}.mp3"
        
        video = VideoFileClip(video_yolu)
        video.audio.write_audiofile(cikis_adi)
        video.close()
        return f"Dönüştürme Başarılı! Dosya: {cikis_adi}"
    except Exception as e:
        return f"Dönüştürme Hatası: {e}"