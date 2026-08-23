import os
import csv

FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))

def load_files(audio_or_text):
    files = [] # directory to store the audio files
    
    if audio_or_text == "text":
        valid_file_formats = (".csv")
    elif audio_or_text == "audio":
        valid_file_formats = (".mp3", ".wav", ".flac")
    
    # iterate through the files in the test_files directory and add them to the list if they are valid formats
    for file in os.listdir(os.path.join(FOLDER_PATH, "test_files")):
        if file.endswith(valid_file_formats):
            files.append(os.path.join(FOLDER_PATH, "test_files", file))

    # if user input is text
    if audio_or_text == "text":
        example_text = []
        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                content = csv.reader(f)
                for row in content:
                    example_text.append(row[0])
        return example_text
    
    # if the user input is not valid, return an empty list
    if audio_or_text not in ["text", "audio"]:
        print("Invalid input. Please enter 'audio' or 'text'.")
        
        return []
    
    # if user input is audio, return the list of audio files
    return files