from pydub import AudioSegment
import audioop  # Correct import for audio operations

def mix_tracks(music_path, voice_path, output_path):
    try:
        music = AudioSegment.from_file(music_path)
        voice = AudioSegment.from_file(voice_path)
        
        # Adjust volume levels for better mixing
        music = music - 5  # Lower music volume slightly
        voice = voice + 2  # Boost voice volume slightly
        
        mixed = music.overlay(voice)
        mixed.export(output_path, format="wav")
    except Exception as e:
        raise Exception(f"Audio mixing failed: {str(e)}")
