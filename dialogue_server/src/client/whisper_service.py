import dotenv
dotenv.load_dotenv()
import os
import openai

def convert_to_text(audio_data):
    transcript = {}
    try:
        openai.api_key = os.environ["OPENAI_API_KEY"]
        transcript = openai.Audio.transcribe("whisper-1", audio_data)
    except Exception as e:
        transcript["text"] = "The whisper service is currently unavailable."
    return transcript["text"]
    
def test_convert_to_text():
    audio_file = open("output.m4a", "rb")
    print(convert_to_text(audio_file))
