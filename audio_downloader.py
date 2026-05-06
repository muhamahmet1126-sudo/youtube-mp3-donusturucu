import yt_dlp
import os

def download_audio(youtube_url):
    # Çerez dosyasının tam yolunu sisteme tanıtıyoruz
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cookie_path = os.path.join(current_dir, 'cookies.txt')
    
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookiefile': cookie_path, # Çerezleri buradan okumasını zorunlu kılıyoruz
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # YouTube engelini aşmak için tarayıcıyı taklit etme
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
    }

    try:
        if not os.path.exists(cookie_path):
            raise Exception("Hata: cookies.txt dosyası GitHub deponda bulunamadı!")
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            return ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
    except Exception as e:
        raise Exception(f"YouTube Erişimi Engellendi: {str(e)}")
