import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [lyrics, setLyrics] = useState('');
  const [musicFile, setMusicFile] = useState(null);
  const [voiceFile, setVoiceFile] = useState(null);
  const [trackUrl, setTrackUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_URL = 'https://lyricbeats.onrender.com';

  const handleGenerate = async () => {
    if (!lyrics.trim()) {
      setError('Please enter lyrics');
      return;
    }
    if (lyrics.length > 3000) {
      setError('Lyrics must be under 3000 characters');
      return;
    }
    if (!musicFile || !voiceFile) {
      setError('Please upload both music and voice files');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('lyrics', lyrics);
    formData.append('music_file', musicFile);
    formData.append('voice_file', voiceFile);

    try {
      const res = await axios.post(`${API_URL}/generate`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setTrackUrl(`${API_URL}${res.data.url}`);
    } catch (err) {
      setError(`Generation failed: ${err.response?.data?.error || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto mt-10 px-4 font-sans">
      <h1 className="text-4xl font-bold mb-6 text-center text-blue-600">🎶 LyricBeats AI</h1>

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      <textarea
        className="w-full h-48 p-4 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800 placeholder-gray-400"
        maxLength={3000}
        value={lyrics}
        onChange={(e) => setLyrics(e.target.value)}
        placeholder="Enter your lyrics here (max 3000 characters)"
      />

      <div className="mt-6 flex flex-col gap-4">
        <div>
          <label className="font-semibold text-gray-700 block mb-1">Upload Music (WAV):</label>
          <input
            type="file"
            accept="audio/wav"
            onChange={(e) => setMusicFile(e.target.files[0])}
            className="w-full p-2 border border-gray-300 rounded-lg"
          />
        </div>

        <div>
          <label className="font-semibold text-gray-700 block mb-1">Upload Voice (WAV):</label>
          <input
            type="file"
            accept="audio/wav"
            onChange={(e) => setVoiceFile(e.target.files[0])}
            className="w-full p-2 border border-gray-300 rounded-lg"
          />
        </div>
      </div>

      <button
        onClick={handleGenerate}
        className="mt-6 px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-blue-300 transition-colors"
        disabled={loading}
      >
        {loading ? 'Generating...' : 'Generate Music'}
      </button>

      {trackUrl && (
        <div className="mt-8">
          <h2 className="text-2xl font-semibold mb-3 text-gray-800">Generated Music:</h2>
          <audio
            controls
            src={trackUrl}
            className="w-full"
            onError={() => setError('Failed to load audio track. Please try again.')}
          />
        </div>
      )}

      <p className="mt-4 text-sm text-gray-500 text-center">
        Character count: {lyrics.length}/3000
      </p>
    </div>
  );
}

export default App;
