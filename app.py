import os
import tempfile
import imageio_ffmpeg

# Point whisper to the exact ffmpeg binary
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
ffmpeg_dir = os.path.dirname(ffmpeg_exe)

# Create a symlink named 'ffmpeg' pointing to the actual binary
symlink_path = os.path.join(ffmpeg_dir, 'ffmpeg')
if not os.path.exists(symlink_path):
    os.symlink(ffmpeg_exe, symlink_path)

os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]

import whisper
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'flac', 'ogg', 'webm'}

print("Loading Whisper model...")
model = whisper.load_model("tiny")
print("Model loaded successfully!")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/transcribe/file', methods=['POST'])
def transcribe_file():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': f'Unsupported file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400

    suffix = '.' + secure_filename(file.filename).rsplit('.', 1)[1].lower()
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        result = model.transcribe(tmp_path)
        return jsonify({
            'text': result['text'].strip(),
            'language': result.get('language', 'unknown')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.unlink(tmp_path)


@app.route('/transcribe/microphone', methods=['POST'])
def transcribe_microphone():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio data provided'}), 400

    audio_file = request.files['audio']

    with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as tmp:
        audio_file.save(tmp.name)
        tmp_path = tmp.name

    try:
        result = model.transcribe(tmp_path)
        return jsonify({
            'text': result['text'].strip(),
            'language': result.get('language', 'unknown')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.unlink(tmp_path)

@app.route('/debug')
def debug():
    import shutil
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    ffmpeg_which = shutil.which('ffmpeg')
    current_path = os.environ.get('PATH', '')
    return jsonify({
        'imageio_ffmpeg_path': ffmpeg_path,
        'ffmpeg_which': ffmpeg_which,
        'PATH': current_path
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
