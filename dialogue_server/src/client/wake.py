import dotenv

dotenv.load_dotenv()
import os
import pvporcupine
import pvrecorder

keyword_model_path = "src\mirror-mirror_en_windows_v3_0_0.ppn"

# initialize Porcupine
access_key = os.environ["PICO_KEY"]
audio_device_index = int(os.environ["AUDIO_INPUT_DEVICE_INDEX"])
handle = pvporcupine.create(
    keyword_paths=[keyword_model_path], sensitivities=[0.5], access_key=access_key
)

# initialize PvRecorder
audio_devices = pvrecorder.PvRecorder.get_available_devices()
recorder = pvrecorder.PvRecorder(
    device_index=-1, frame_length=512
)  # device_index=-1 for default audio input device
recorder.start()


async def listen_for_wake(handle_detection):
    while True:
        pcm = recorder.read()
        keyword_index = handle.process(pcm)
        if keyword_index >= 0:
            await handle_detection()
