// placeholder for frontend App.jsx code
// #------------------ FRONTEND ------------------
// #File: frontend/src/App.jsx
import React, { useState } from 'react';
import axios from 'axios';

function App() {
const [lyrics, setLyrics] = useState("");
const [genre, setGenre] = useState("pop");
const [voice, setVoice] = useState("female");
const [trackUrl, setTrackUrl] = useState(null);
const [loading, setLoading] = useState(false);

const handleGenerate = async () => {
if (!lyrics.trim()) return;
setLoading(true);
try {
const res = await axios.post('http://localhost:5000/generate', {
lyrics,
genre,
voice,
});
setTrackUrl('http://localhost:5000' + res.data.url);
} catch (err) {
alert('Generation failed');
} finally {
setLoading(false);
}
};

return (

🎶 LyricBeats AI
<textarea
className="w-full h-40 p-2 border border-gray-300 rounded"
maxLength={3000}
value={lyrics}
onChange={(e) => setLyrics(e.target.value)}
placeholder="Enter your lyrics here (max 3000 characters)"
/>

Genre:
<select value={genre} onChange={(e) => setGenre(e.target.value)} className="ml-2 border p-1">
Pop
Hip Hop
R&B
EDM

    <label className="ml-4">Voice:</label>
    <select value={voice} onChange={(e) => setVoice(e.target.value)} className="ml-2 border p-1">
      <option value="female">Female</option>
      <option value="male">Male</option>
    </select>
  </div>
  <button
    onClick={handleGenerate}
    className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
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
