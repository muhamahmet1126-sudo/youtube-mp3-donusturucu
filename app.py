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
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "Lütfen bir URL girin!", 400

    # Format hatasını çözmek için daha esnek hale getirilmiş yt-dlp ayarları
    ydl_opts = {
        # 'bestaudio' yerine sadece 'best' diyerek en uygun olanı bulmasını sağlıyoruz
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),
        # Bot engelini aşmak için eklediğin cookies.txt dosyasını kullanır
        'cookiefile': 'cookies.txt',
        'quiet': True,
        'no_warnings': True,
        # Bazı format hatalarını görmezden gelerek indirmeye devam eder
        'ignoreerrors': True,
        'nocheckcertificate': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Video bilgilerini çıkar ve indir
            info = ydl.extract_info(url, download=True)
            if info is None:
                return "Video bilgileri alınamadı veya format uygun değil.", 400
                
            # Dosya adını belirle ve mp3 uzantısını garantiye al
            file_path = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"
            
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return f"Hata oluştu: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
