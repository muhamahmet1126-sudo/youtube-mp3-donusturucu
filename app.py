from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import imageio_ffmpeg # FFmpeg sorununu çözmek için ekledik

app = Flask(__name__)

# İndirilen dosyaların geçici olarak tutulacağı klasör
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    # Bu rota ana sayfanın açılmasını sağlar (image_87ba51.png içindeki index.html'i çağırır)
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "Lütfen bir URL girin!", 400

    # yt-dlp ayarları
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        # imageio-ffmpeg sayesinde ffmpeg yolunu otomatik bulur
        'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe() 
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return f"Hata oluştu: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
