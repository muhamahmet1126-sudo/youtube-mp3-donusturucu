import yt_dlp
import os

def download_audio(youtube_url):
    cookie_path = os.path.join(os.getcwd(), 'cookies.txt')
    
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    ydl_opts = {
        # Format seçimini en garanti hale getirdik
        'format': 'ba/b', 
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookiefile': cookie_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # YouTube'u kandırmak için güncel tarayıcı kimliği
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Önce videonun indirilebilir olup olmadığını kontrol et
            info = ydl.extract_info(youtube_url, download=True)
            return ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
    except Exception as e:
        raise Exception(f"YouTube Erişimi Engellendi: {str(e)}")
