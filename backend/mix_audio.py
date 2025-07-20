# placeholder for audio mixing
#File: backend/mix_audio.py
from pydub import AudioSegment

def mix_tracks(music_path, voice_path, output_path):
  music = AudioSegment.from_file(music_path)
  voice = AudioSegment.from_file(voice_path)
  
  mixed = music.overlay(voice)
  mixed.export(output_path, format="wav")
