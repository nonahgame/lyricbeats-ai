# LyricBeatsAI 🎶

An AI music generator that takes lyrics, selects genre and voice type (male/female), and generates original tracks.

## Features
- Up to 3000-character lyrics input
- Genre selection: Pop, Hip Hop, R&B, EDM
- Male or Female voice synthesis
- Uses MusicGen + Bark (open-source AI)
- Frontend: React + Tailwind CSS
- Backend: Flask (Python)
- Deploys on Render.com
- Public GitHub project

## Project Structure
- `/backend`: Flask API + MusicGen + Bark
- `/frontend`: React app interface

## Deployment
- Backend & frontend deployable as separate Render services
- Replace API base URLs accordingly

## TODO
- Replace wrapper logic with real MusicGen + Bark integration
- Add Firebase or Flask-Login auth
