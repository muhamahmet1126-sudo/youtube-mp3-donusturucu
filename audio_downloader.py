import yt_dlp

def mp3_indir(url):
    ayarlar = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }
    
    try:
        with yt_dlp.YoutubeDL(ayarlar) as ydl:
            ydl.download([url])
        return "İndirme ve Dönüştürme Başarılı!"
    except Exception as e:
        return f"İndirme Hatası: {e}"