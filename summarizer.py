import os
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()


def process_meeting(transcript, user_prompt):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing from the .env file."
        )

    client = genai.Client(
        api_key=api_key
    )

    prompt = f"""
You are a meeting analysis assistant.

Follow the user's instruction using only the information
given in the meeting transcript.

Do not invent information that is not present in the transcript.

USER INSTRUCTION:
{user_prompt}

MEETING TRANSCRIPT:
{transcript}
"""

    models = [
        "gemini-3.7-flash",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite"
    ]

    last_error = None

    for model_name in models:

        print(f"Trying model: {model_name}")

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                return response.text

            except Exception as error:

                last_error = error

                print(
                    f"Attempt {attempt + 1} failed: {error}"
                )

                
                if attempt < 2:

                    delay = 2 ** attempt

                    print(
                        f"Retrying in {delay} seconds..."
                    )

                    time.sleep(delay)

        print(
            f"{model_name} failed. Trying next model..."
        )

    raise Exception(
        f"Gemini is currently unavailable. "
        f"Please try again later. Details: {last_error}"
    )