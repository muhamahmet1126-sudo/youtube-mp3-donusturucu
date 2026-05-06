from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import imageio_ffmpeg

app = Flask(__name__)

# İndirilen dosyaların geçici olarak tutulacağı klasör
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    # Ana sayfanın açılmasını sağlayan rota
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
        'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),
        # YouTube bot engelini aşmak için eklediğimiz çerez dosyası
        'cookiefile': 'cookies.txt',
        'quiet': True,
        'no_warnings': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # Dosya uzantısını mp3 olarak ayarla
            file_path = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"
            
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        # Eğer hata oluşursa ekranda nedenini görelim
        return f"Hata oluştu: {str(e)}", 500

if __name__ == '__main__':
    # Render'da port sorunu yaşamamak için default ayarlar
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
