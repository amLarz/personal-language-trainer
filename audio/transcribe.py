import whisper

def transcribe_audio(audio):
    # download the model and get result
    model = whisper.load_model("base")
    result = model.transcribe(audio)
    
    return result["text"]