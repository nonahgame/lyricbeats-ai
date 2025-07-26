from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
import logging  # Added for debugging
from musicgen_wrapper import generate_music
from bark_wrapper import generate_voice
from mix_audio import mix_tracks

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = 'generated_tracks'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    lyrics = data.get('lyrics')
    genre = data.get('genre')
    voice = data.get('voice')

    logging.info(f"Received request: lyrics={len(lyrics)} chars, genre={genre}, voice={voice}")

    # Validate input
    if not lyrics or not genre or not voice:
        logging.error("Missing required fields")
        return jsonify({'error': 'Missing lyrics, genre, or voice'}), 400
    if len(lyrics) > 3000:
        logging.error("Lyrics exceed character limit")
        return jsonify({'error': 'Lyrics exceed 3000 characters'}), 400

    try:
        filename_base = str(uuid.uuid4())
        logging.debug(f"Generated filename base: {filename_base}")

        # Step 1: Generate instrumentals
        instrumental_path = os.path.join(UPLOAD_FOLDER, f"{filename_base}_music.wav")
        logging.debug(f"Generating music at: {instrumental_path}")
        generate_music(lyrics, genre, instrumental_path)

        # Step 2: Generate voice
        voice_path = os.path.join(UPLOAD_FOLDER, f"{filename_base}_voice.wav")
        logging.debug(f"Generating voice at: {voice_path}")
        generate_voice(lyrics, voice, voice_path)

        # Step 3: Mix voice and instrumentals
        output_path = os.path.join(UPLOAD_FOLDER, f"{filename_base}_final.wav")
        logging.debug(f"Mixing tracks to: {output_path}")
        mix_tracks(instrumental_path, voice_path, output_path)

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
