import os

from dotenv import load_dotenv
from faster_whisper import WhisperModel
from pyannote.audio import Pipeline


load_dotenv()


whisper_model = None
diarization_pipeline = None


def load_whisper_model():

    global whisper_model

    if whisper_model is None:

        print("Loading Whisper model...")

        whisper_model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

    return whisper_model


def load_diarization_pipeline():

    global diarization_pipeline

    if diarization_pipeline is None:

        print("Loading speaker diarization model...")

        hf_token = os.getenv("HF_TOKEN")

        if not hf_token:

            raise ValueError(
                "HF_TOKEN is missing from the .env file."
            )

        diarization_pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            token=hf_token
        )

    return diarization_pipeline


def get_speaker_for_segment(
    start,
    end,
    speaker_segments
):

    best_speaker = "Speaker Unknown"

    best_overlap = 0


    for speaker_start, speaker_end, speaker in speaker_segments:

        overlap_start = max(
            start,
            speaker_start
        )

        overlap_end = min(
            end,
            speaker_end
        )

        overlap = max(
            0,
            overlap_end - overlap_start
        )

        if overlap > best_overlap:

            best_overlap = overlap

            best_speaker = speaker


    return best_speaker


def transcribe_audio(audio_path):

    model = load_whisper_model()

    pipeline = load_diarization_pipeline()


    print("Transcribing audio...")


    whisper_segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        word_timestamps=False
    )


    whisper_segments = list(
        whisper_segments
    )


    print("Identifying speakers...")


    diarization = pipeline(
        audio_path
    )


    # Get the actual speaker annotation
    diarization_annotation = diarization.speaker_diarization


    speaker_segments = []


    for turn, _, speaker in diarization_annotation.itertracks(
        yield_label=True
    ):

        speaker_segments.append(
            (
                turn.start,
                turn.end,
                speaker
            )
        )


    speaker_mapping = {}

    speaker_count = 1


    transcript_parts = []


    for segment in whisper_segments:

        speaker = get_speaker_for_segment(
            segment.start,
            segment.end,
            speaker_segments
        )


        if speaker not in speaker_mapping:

            speaker_mapping[speaker] = (
                f"Speaker {speaker_count}"
            )

            speaker_count += 1


        speaker_name = speaker_mapping[speaker]


        text = segment.text.strip()


        if text:

            transcript_parts.append(
                f"{speaker_name}: {text}"
            )


    transcript = "\n\n".join(
        transcript_parts
    )


    return transcript