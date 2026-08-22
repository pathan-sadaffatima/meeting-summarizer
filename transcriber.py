from faster_whisper import WhisperModel


model = None


def load_model():
    global model

    if model is None:
        print("Loading Whisper model...")

        model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

    return model


def transcribe_audio(audio_path):
    model = load_model()

    print("Transcribing audio...")

    segments, info = model.transcribe(
        audio_path,
        beam_size=5
    )

    transcript_parts = []

    for segment in segments:
        transcript_parts.append(segment.text.strip())

    transcript = " ".join(transcript_parts)

    return transcript