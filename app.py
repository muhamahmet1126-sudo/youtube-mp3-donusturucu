import yt_dlp
import os

def download_audio(youtube_url):
    # Çerez dosyasının varlığını kontrol et
    cookie_file = 'cookies.txt'
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        # YouTube engelini aşmak için çerezleri kullanıyoruz
        'cookiefile': cookie_file if os.path.exists(cookie_file) else None,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # Sunucu kimliğini gizlemek için bazı ek ayarlar
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            return ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
    except Exception as e:
        # Eğer hala hata alırsak detayını görelim
        raise Exception(f"İndirme Hatası: {str(e)}")
