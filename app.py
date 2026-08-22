import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from transcriber import transcribe_audio
from summarizer import process_meeting


app = Flask(__name__)

app.secret_key = "meeting-summarizer-secret-key"

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = {
    "mp3",
    "wav",
    "m4a",
    "mp4",
    "aac",
    "ogg",
    "flac"
}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "audio" not in request.files:

        flash("Please select an audio file.")

        return redirect(url_for("index"))


    file = request.files["audio"]

    user_prompt = request.form.get("prompt")


    if file.filename == "":

        flash("No audio file selected.")

        return redirect(url_for("index"))


    if not user_prompt or not user_prompt.strip():

        user_prompt = (
            "Summarize this meeting transcript into "
            "key decisions and action items."
        )


    if not allowed_file(file.filename):

        flash("Unsupported audio format.")

        return redirect(url_for("index"))


    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )


    filename = file.filename

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )


    file.save(file_path)


    try:

        transcript = transcribe_audio(
            file_path
        )


        result = process_meeting(
            transcript,
            user_prompt
        )


        return render_template(
            "result.html",
            filename=filename,
            transcript=transcript,
            result=result,
            user_prompt=user_prompt
        )


    except Exception as error:

        print(error)

        error_message = str(error)

        if "503" in error_message or "UNAVAILABLE" in error_message:

            flash(
                "The AI service is currently busy. "
                "Please wait a moment and try again."
            )

        elif "429" in error_message:

            flash(
                "The API usage limit has been reached. "
                "Please wait and try again later."
            )

        else:

            flash(
                "An error occurred while processing the meeting. "
                "Please try again."
            )

        return redirect(
            url_for("index")
        )


    finally:

        if os.path.exists(file_path):

            try:

                os.remove(file_path)

            except Exception:

                pass


if __name__ == "__main__":

    app.run(
        debug=True
    )