from audio.transcribe import transcribe_audio
from audio.record import recording_audio
from data.db import save_to_database
from nlp.text_processor import process_text

def main(recording, input_type):
    # transcribe audio and get result
    text = recording if input_type == "text" else transcribe_audio(recording)
    print("Transcribed Text:", text)

    # process the transcribed text
    processed_text = process_text(text)
    print("Processed Text:", processed_text)

    # update the word frequency in the database 
    print(save_to_database(processed_text))
    
if __name__ == "__main__":
    main(recording_audio(), input_type="audio")  # Call the main function with the recorded audio