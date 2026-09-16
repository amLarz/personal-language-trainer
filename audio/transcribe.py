import whisper

# download the model
model = whisper.load_model("base")


def transcribe_audio(audio):
    # get tge result of the transcription
    result = model.transcribe(audio)

    return result["text"]
