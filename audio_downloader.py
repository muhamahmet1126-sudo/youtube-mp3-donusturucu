import yt_dlp
import os

def download_audio(youtube_url):
    cookie_path = os.path.join(os.getcwd(), 'cookies.txt')
    
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    ydl_opts = {
        # 'bestaudio' yerine 'ba' (best audio) ve 'b' (best) kullanarak esnekliği artırıyoruz
        'format': 'ba/b',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookiefile': cookie_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # YouTube bot korumasını aşmak için ek parametreler
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'prefer_ffmpeg': True,
        # Format hatasını önlemek için youtube-dl uyumluluğunu artırıyoruz
        'youtube_include_dash_manifest': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Video bilgilerini al ve indir
            info = ydl.extract_info(youtube_url, download=True)
            # Dosya adını belirle
            filename = ydl.prepare_filename(info)
            # Uzantıyı mp3 olarak düzelt (Postprocessor sonrası isim değişeceği için)
            base, _ = os.path.splitext(filename)
            return f"{base}.mp3"
    except Exception as e:
        raise Exception(f"YouTube Erişimi Engellendi: {str(e)}")
