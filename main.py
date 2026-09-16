from audio.record import recording_audio
from audio.transcribe import transcribe_audio
from data.db import save_and_fetch
from scoring.stat_scoring import stat_scoring
from nlp.text_processor import process_text
#from translation.translate import translate_record

def main(recording, input_type):
    # transcribe audio and get result
    text = recording if input_type == "text" else transcribe_audio(recording)
    print("Transcribed Text:", text)

    # process the transcribed text
    processed_text = process_text(text)
    print("Processed Text:", processed_text)

    # update the word frequency in the database
    word_snapshot = save_and_fetch(processed_text)
    print("Snapshot:", word_snapshot)

    # statistical scoring and translation of the processed text
    stat_scoring(word_snapshot)
    #translate_record(processed_text)


if __name__ == "__main__":
    main(recording_audio(), input_type="audio")  # Call the main function with the recorded audio
