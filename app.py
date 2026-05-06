import yt_dlp
import os

def download_audio(youtube_url):
    # Çerez dosyasının tam yolunu belirleyelim
    cookie_path = os.path.join(os.getcwd(), 'cookies.txt')
    
    # İndirme klasörünü garantiye alalım
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        # Çerez dosyasını zorunlu olarak kullanıyoruz
        'cookiefile': cookie_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # YouTube'u kandırmak için gerçek tarayıcı kimlikleri
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'
    }

    try:
        # Eğer cookies.txt yoksa hata verip durmasını engelleyelim
        if not os.path.exists(cookie_path):
            raise Exception("cookies.txt dosyası bulunamadı! Lütfen GitHub'a yükleyin.")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            return ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
    except Exception as e:
        raise Exception(f"İndirme Hatası: {str(e)}")
