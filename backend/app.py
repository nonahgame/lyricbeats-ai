from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = 'generated_tracks'
ALLOWED_EXTENSIONS = {'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/generate', methods=['POST'])
def generate():
    logging.info("Received /generate request")

    # Validate lyrics
    lyrics = request.form.get('lyrics')
    if not lyrics:
        logging.error("Missing lyrics")
        return jsonify({'error': 'Missing lyrics'}), 400
    if len(lyrics) > 3000:
        logging.error("Lyrics exceed character limit")
        return jsonify({'error': 'Lyrics exceed 3000 characters'}), 400

    # Validate file uploads
    if 'music_file' not in request.files or 'voice_file' not in request.files:
        logging.error("Missing music or voice file")
        return jsonify({'error': 'Missing music or voice file'}), 400

    music_file = request.files['music_file']
    voice_file = request.files['voice_file']

    if music_file.filename == '' or voice_file.filename == '':
        logging.error("No selected file")
        return jsonify({'error': 'No selected file'}), 400

    if not (allowed_file(music_file.filename) and allowed_file(voice_file.filename)):
        logging.error("Invalid file format; only WAV files allowed")
        return jsonify({'error': 'Invalid file format; only WAV files allowed'}), 400

    try:
        filename_base = str(uuid.uuid4())
        logging.debug(f"Generated filename base: {filename_base}")

        # Save uploaded files
        music_filename = f"{filename_base}_music.wav"
        voice_filename = f"{filename_base}_voice.wav"
        music_path = os.path.join(app.config['UPLOAD_FOLDER'], music_filename)
        voice_path = os.path.join(app.config['UPLOAD_FOLDER'], voice_filename)

        logging.debug(f"Saving music file to: {music_path}")
        music_file.save(music_path)
        logging.debug(f"Saving voice file to: {voice_path}")
        voice_file.save(voice_path)

        # Verify files exist
        if not os.path.exists(music_path) or not os.path.exists(voice_path):
            logging.error("Failed to save uploaded files")
            return jsonify({'error': 'Failed to save uploaded files'}), 500

        # Mix audio
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename_base}_final.wav")
        logging.debug(f"Mixing tracks to: {output_path}")
        from mix_audio import mix_tracks
        mix_tracks(music_path, voice_path, output_path)

        logging.info(f"Track generated successfully: {output_path}")
        return jsonify({'url': f"/tracks/{filename_base}_final.wav"})
    except Exception as e:
        logging.error(f"Generation failed: {str(e)}", exc_info=True)
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

@app.route('/tracks/<filename>')
def serve_track(filename):
    try:
        logging.debug(f"Serving track: {filename}")
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        logging.error(f"Track not found: {filename}")
        return jsonify({'error': 'Track not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
