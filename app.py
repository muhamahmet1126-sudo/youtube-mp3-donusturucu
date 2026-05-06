from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import imageio_ffmpeg

app = Flask(__name__)

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

    # Çerez dosyasının tam yolunu garantiye alıyoruz
    cookie_path = os.path.join(os.path.dirname(__file__), 'cookies.txt')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),
        'cookiefile': cookie_path, # Tam yol kullanıldı
        'quiet': False,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # İndirilen dosyanın adını yakala
            filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"
            return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Hata oluştu: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
