# python script for executing whisper transcription on a directory of audio files, excluding previously transcribed files

import os
import subprocess
import sys
import logging

WHISPER_MODEL = "base.en"
LANGUAGE = "English"
DIRECTORY = "/home/lewis/Projects/podwhisper/allcasts/patreon_downloader/redscare"

# start logging 
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# confirm directory exists
if not os.path.isdir(DIRECTORY):
    print("Directory does not exist.")
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
    # execute whisper command and print output
    subprocess.run(["whisper", file, "--model", WHISPER_MODEL, "--language", LANGUAGE])
    logging.info(f"Transcription complete for {file}")

