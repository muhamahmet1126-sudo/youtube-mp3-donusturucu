from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import imageio_ffmpeg
import logging

app = Flask(__name__)

# Logları takip etmek için (Render panelinde hataları görmek için)
logging.basicConfig(level=logging.INFO)

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "Lütfen bir URL girin!", 400

    # En güncel bot aşma ve format ayarları
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),
        'cookiefile': 'cookies.txt',
        'quiet': False, # Hataları loglarda görebilmek için açtık
        'no_warnings': False,
        'nocheckcertificate': True,
        'add_header': [
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 1. Aşama: Bilgileri al ve indir
            info = ydl.extract_info(url, download=True)
            
            # 2. Aşama: Dosya yolunu oluştur (Uzantıyı manuel garantiye al)
            title = info.get('title', 'video')
            # Klasör içindeki dosyaları tara ve en yeni inen .mp3'ü bul
            # (Bu yöntem, isimdeki garip karakterlerden kaynaklanan hataları çözer)
            files = [os.path.join(DOWNLOAD_FOLDER, f) for f in os.listdir(DOWNLOAD_FOLDER)]
            latest_file = max(files, key=os.path.getctime)
            
            return send_file(latest_file, as_attachment=True)
            
    except Exception as e:
        logging.error(f"Sistem Hatası: {str(e)}")
        return f"Hata oluştu: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
