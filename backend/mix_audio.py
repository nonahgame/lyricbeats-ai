from pydub import AudioSegment
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def mix_tracks(music_path, voice_path, output_path):
    try:
        logging.debug(f"Loading music file: {music_path}")
        music = AudioSegment.from_file(music_path, format="wav")
        
        logging.debug(f"Loading voice file: {voice_path}")
        voice = AudioSegment.from_file(voice_path, format="wav")
        
        # Adjust volume levels for better mixing
        music = music - 5  # Lower music volume
        voice = voice + 2  # Boost voice volume
        
        logging.debug(f"Mixing tracks to: {output_path}")
        mixed = music.overlay(voice)
        mixed.export(output_path, format="wav")
        logging.info(f"Tracks mixed successfully: {output_path}")
    except Exception as e:
        logging.error(f"Audio mixing failed: {str(e)}", exc_info=True)
        raise Exception(f"Audio mixing failed: {str(e)}")
