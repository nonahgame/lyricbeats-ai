# placeholder for Flask app.py
# 2nd step
#File: backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
from musicgen_wrapper import generate_music
from bark_wrapper import generate_voice
from mix_audio import mix_tracks

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'generated_tracks'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/generate', methods=['POST'])
def generate():
  data = request.json
  lyrics = data.get('lyrics')
  genre = data.get('genre')
  voice = data.get('voice')
  
  if not lyrics or not genre or not voice:
      return jsonify({'error': 'Missing data'}), 400
  
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

@app.route('/tracks/')
def serve_track(filename):
  return app.send_static_file(os.path.join('generated_tracks', filename))

if __name__ == '__main__':
  app.run(debug=True, port=5000)
