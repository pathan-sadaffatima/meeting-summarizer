# Meeting Summarizer

A web application that converts meeting audio into text and uses Gemini to analyze the meeting based on a user-provided prompt.

## Features

- Upload meeting audio
- Convert audio to text using Faster-Whisper
- Enter a custom prompt for meeting analysis
- Generate summaries, decisions, action items, or other requested information
- View the generated result and full transcript

## Technologies Used

- Python
- Flask
- Faster-Whisper
- Google Gemini API
- HTML and CSS

## Project Structure

```text
meeting-summarizer/
├── app.py
├── transcriber.py
├── summarizer.py
├── requirements.txt
├── demo/
├── templates/
└── static/