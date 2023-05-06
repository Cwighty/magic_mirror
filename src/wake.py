import dotenv

dotenv.load_dotenv()
import os
import pvporcupine
import pvrecorder

# specify the keyword path for the English language
keyword_path = 'src\mirror-mirror_en_windows_v2_1_0.ppn'

# specify your Picovoice access key
# initialize Porcupine
access_key = os.environ["PICO_KEY"]
handle = pvporcupine.create(keyword_paths=[keyword_path], sensitivities=[0.5], access_key=access_key)
# initialize PvRecorder
recorder = pvrecorder.PvRecorder(device_index=0, frame_length=512)
recorder.start()

# listen for the wake word
def listen_for_wake(handle_detection):
    pcm = recorder.read()
    keyword_index = handle.process(pcm)
    if keyword_index >= 0:
        handle_detection()