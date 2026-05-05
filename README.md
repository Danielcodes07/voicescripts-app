# VoiceScript — Speech Recognition App

A full-stack speech-to-text app powered by **OpenAI Whisper** and **Flask**.

## Features
- 🎵 **Upload audio files** — MP3, WAV, M4A, FLAC, OGG (up to 50MB)
- 🎤 **Live microphone recording** — record directly in the browser
- 🌍 **Auto language detection** — Whisper detects and displays the language
- 📋 **Copy to clipboard** — one-click copy of transcribed text
- 🔒 **Fully offline** — no data sent to external servers

## Model Size vs Speed

Edit `app.py` line: `model = whisper.load_model("base")`

| Model  | Size   | Speed  | Accuracy |
|--------|--------|--------|----------|
| tiny   | 75 MB  | Fastest| Good     |
| base   | 145 MB | Fast   | Better   |
| small  | 465 MB | Medium | Great    |
| medium | 1.5 GB | Slow   | Excellent|
| large  | 3 GB   | Slowest| Best     |

## Project Structure
```
speech_app/
├── app.py               # Flask backend
├── requirements.txt     # Python dependencies
├── README.md
└── templates/
    └── index.html       # Frontend UI
```
