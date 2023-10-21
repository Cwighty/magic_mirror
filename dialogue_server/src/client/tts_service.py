import dotenv
dotenv.load_dotenv()
from pprint import pprint
from datetime import datetime
import os
import requests
API_KEY = os.environ["ELEVEN_LAB_KEY"]

def get_text_to_speech(text):
    """
    Get text to speech from ElevenLabs
    :param text: text to convert
    :return: file name of the audio file
    """
    VOICE = os.environ["ELEVEN_LAB_VOICE"]
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}"

    #generate a random file name with date and time 
    filename = f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"

    body ={
        "text": text,
        "voice_settings": {
            "stability": .7,
            "similarity_boost": .5
            }
        }

    headers = {
        "accept": "application/json",
        "xi-api-key": f"{API_KEY}"
    }
    #make a post request to the API
    response = requests.post(url, json=body, headers=headers)
    #save the audio file from the stream
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
            return filename
    else:
        print("Error:", response.status_code, response.text)
        return None
def list_voices():
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {
        "accept": "application/json",
        "xi-api-key": f"{API_KEY}"
    }
    response = requests.get(url, headers=headers)
    pprint(response.json())

def print_voice(voice_id):
    url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
    headers = {
        "accept": "application/json",
        "xi-api-key": f"{API_KEY}"
    }
    response = requests.get(url, headers=headers)
    pprint(response.json()) 

def play_audio(filename):
    # play mp3 audio file
    import pygame
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
