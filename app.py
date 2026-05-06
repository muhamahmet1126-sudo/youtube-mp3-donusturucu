from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# İndirilen dosyaların geçici olarak tutulacağı klasör
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/indir', methods=['POST'])
def indir():
    url = request.form.get('url')
    tip = request.form.get('tip')
    
    if not url:
        return "Lütfen bir link girin!", 400

    # yt-dlp ayarları
    if tip == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        }
    else:
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if tip == 'mp3':
                filename = filename.rsplit('.', 1)[0] + '.mp3'
            
            # Dosyayı kullanıcıya gönder
            return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Hata oluştu: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)