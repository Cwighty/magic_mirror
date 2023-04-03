from pprint import pprint
import dotenv
import numpy as np
dotenv.load_dotenv()
import os
import pvporcupine
import pvrecorder
import resampy
import scipy.signal as signal
from audio_service import record_audio, write_audio_to_file
from whisper_service import convert_to_text

# set the wake word to "mirror"
wake_word = "mirror"

# specify the keyword path for the English language
keyword_path = 'src\mirror-mirror_en_windows_v2_1_0.ppn'

# specify your Picovoice access key
# initialize Porcupine
access_key = os.environ["PICO_KEY"]
handle = pvporcupine.create(keyword_paths=[keyword_path], sensitivities=[0.5], access_key=access_key)

# define a function to handle the wake word detection event
def handle_detection():
    print("Keyword detected!")
    frames, rate = record_audio()
    write_audio_to_file(frames, rate, "output.wav")
    # print("Transcribing audio...")
    # audio_file= open("output.wav", "rb")
    # text = convert_to_text(audio_file)
    # print("Transcription:", text)
# define a resampling function

# initialize PvRecorder
recorder = pvrecorder.PvRecorder(device_index=0, frame_length=512)
recorder.start()

# listen for the wake word
while True:
    pcm = recorder.read()
    keyword_index = handle.process(pcm)
    if keyword_index >= 0:
        handle_detection()


