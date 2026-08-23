# Meeting Summarizer

A web application that converts meeting audio into a speaker-labelled transcript and uses Google Gemini to analyze the meeting based on a user-provided prompt.

The application allows users to upload a meeting recording, automatically transcribe the audio using Faster-Whisper, identify different speakers using Pyannote speaker diarization, and generate an AI-powered summary or other requested analysis using Google Gemini.

## Features

- Upload meeting audio files
- Supports MP3, WAV, M4A, MP4, AAC, OGG, and FLAC formats
- Convert meeting audio into text using Faster-Whisper
- Identify and label different speakers using Pyannote speaker diarization
- Generate speaker-labelled transcripts
- Enter a custom prompt for meeting analysis
- Generate summaries, key decisions, action items, responsibilities, or other requested information
- Use Google Gemini API for AI-powered meeting analysis
- Automatically save meeting information and results in an SQLite database
- View the complete transcript and generated analysis
- View previously processed meetings

## Technologies Used

- Python
- Flask
- Faster-Whisper
- Pyannote Audio
- Google Gemini API
- SQLite
- Hugging Face
- HTML
- CSS

## Project Structure

```text
meeting-summarizer/

├── app.py
├── transcriber.py
├── summarizer.py
├── database.py
├── requirements.txt
├── .env
├── meetings.db
│
├── uploads/
│
├── templates/
│   ├── index.html
│   ├── result.html
│   └── history.html
│
├── static/
│   └── style.css
│
└── demo/