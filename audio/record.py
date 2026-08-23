import sounddevice as sd

fs = 16000  # sample rate of whisper.
duration = 5  # seconds

# setting default sample rate and channels for sounddevice
sd.default.samplerate = fs
sd.default.channels = 1
sd.default.dtype = "float32"


def recording_audio():
    print("recording started...")
    # recording audio
    recording = sd.rec(int(duration * fs))
    sd.wait()
    print("recording stopped.")

    return recording.flatten()
