from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
from musicgen_wrapper import generate_music
from bark_wrapper import generate_voice
from mix_audio import mix_tracks

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for development

UPLOAD_FOLDER = 'generated_tracks'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    lyrics = data.get('lyrics')
    genre = data.get('genre')
    voice = data.get('voice')

    # Validate input
    if not lyrics or not genre or not voice:
        return jsonify({'error': 'Missing lyrics, genre, or voice'}), 400
    if len(lyrics) > 3000:
        return jsonify({'error': 'Lyrics exceed 3000 characters'}), 400

    try:
        filename_base = str(uuid.uuid4())

        # Step 1: Generate instrumentals
        instrumental_path = os.path.join(UPLOAD_FOLDER, f"{filename_base}_music.wav")
        generate_music(lyrics, genre, instrumental_path)

        # Step 2: Generate voice
        voice_path = os.path.join(UPLOAD_FOLDER, f"{filename_base}_voice.wav")
        generate_voice(lyrics, voice, voice_path)

        # Step 3: Mix voice and instrumentals
        output_path = os.path.join(UPLOAD_FOLDER, f"{filename_base}_final.wav")
        mix_tracks(instrumental_path, voice_path, output_path)

        return jsonify({'url': f"/tracks/{filename_base}_final.wav"})
    except Exception as e:
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

@app.route('/tracks/<filename>')  # Fixed route to serve tracks
def serve_track(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        return jsonify({'error': 'Track not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
