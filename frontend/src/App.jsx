// File: frontend/src/App.jsx

import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [lyrics, setLyrics] = useState('');
  const [genre, setGenre] = useState('pop');
  const [voice, setVoice] = useState('female');
  const [trackUrl, setTrackUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  // ✅ Your backend URL on Render
  const API_URL = 'https://lyricbeats.onrender.com';

  const handleGenerate = async () => {
    if (!lyrics.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/generate`, {
        lyrics,
        genre,
        voice,
      });
      setTrackUrl(`${API_URL}${res.data.url}`);
    } catch (err) {
      console.error('Generation failed:', err.message);
      alert('Generation failed. Check server logs or input.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-10 px-4">
      <h1 className="text-3xl font-bold mb-4 text-center">🎶 LyricBeats AI</h1>

      <textarea
        className="w-full h-40 p-2 border border-gray-300 rounded"
        maxLength={3000}
        value={lyrics}
        onChange={(e) => setLyrics(e.target.value)}
        placeholder="Enter your lyrics here (max 3000 characters)"
      />

      <div className="mt-4">
        <label className="font-semibold">Genre:</label>
        <select
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
          className="ml-2 border p-1 rounded"
        >
          <option value="pop">Pop</option>
          <option value="hiphop">Hip Hop</option>
          <option value="rnb">R&B</option>
          <option value="edm">EDM</option>
        </select>

        <label className="ml-4 font-semibold">Voice:</label>
        <select
          value={voice}
          onChange={(e) => setVoice(e.target.value)}
          className="ml-2 border p-1 rounded"
        >
          <option value="female">Female</option>
          <option value="male">Male</option>
        </select>
      </div>

      <button
        onClick={handleGenerate}
        className="mt-6 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        disabled={loading}
      >
        {loading ? 'Generating...' : 'Generate Music'}
      </button>

      {trackUrl && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold mb-2">Generated Music:</h2>
          <audio controls src={trackUrl} className="w-full" />
        </div>
      )}
    </div>
  );
}

export default App;
