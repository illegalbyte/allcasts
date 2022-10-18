# python script for executing whisper transcription on a directory of audio files, excluding previously transcribed files

import os
import subprocess
import sys
import logging

WHISPER_MODEL = "base.en"
LANGUAGE = "English"

# ask for directory
directory = input("Enter directory of audio files: ")
# verify directory
if not os.path.isdir(directory):
    logging.critical("Directory not found.")
    sys.exit()

# get a list of .mp3, .wav, and .m4a files in the current directory
files = [f for f in os.listdir(".") if f.endswith((".mp3", ".wav", ".m4a"))]
# get a list of .txt files in the current directory
transcribed_files = [f for f in os.listdir(".") if f.endswith(".txt")]

# iterate through the list of audio files which have not been transcribed
for file in files:
    if file[:-4] + ".txt" in transcribed_files:
        logging.info(f"Skipping {file} because it has already been transcribed.")
        continue
    logging.info(f"Transcribing {file}")
    # execute whisper command
    subprocess.run(["whisper", "--model", WHISPER_MODEL, "--language", LANGUAGE])
    logging.info(f"Transcription complete for {file}")

