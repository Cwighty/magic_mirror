# listen for the wake word
from audio_service import record_audio, write_audio_to_file
from llm_service import get_ai_response
from tts_service import get_text_to_speech, play_audio
from wake import listen_for_wake
from whisper_service import convert_to_text




# define a function to handle the wake word detection event
def handle_detection():
    print("Keyword detected!")
    frames, rate = record_audio()
    write_audio_to_file(frames, rate, "output.wav")
    print("Transcribing audio...")
    audio_file= open("output.wav", "rb")
    text = convert_to_text(audio_file)
    print("Transcription:", text)
    ai_res = get_ai_response(text)
    tts_audio = get_text_to_speech(ai_res)
    print("Playing audio...")
    play_audio(tts_audio)

while True:
    listen_for_wake(handle_detection)