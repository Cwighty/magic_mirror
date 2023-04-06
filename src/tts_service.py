from datetime import datetime
import dotenv
dotenv.load_dotenv()
import os
import requests

def get_text_to_speech(text):
    """
    Get text to speech from ElevenLabs
    :param text: text to convert
    :return: file name of the audio file
    """
    API_KEY = os.environ["ELEVEN_LAB_KEY"]
    VOICE = os.environ["VOICE"]
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
    #make a post request to the API
    response = requests.post(url, json=body, headers={"x-api-key": API_KEY})
    #save the audio file from the stream
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
            return filename
    else:
        print("Error:", response.status_code, response.text)
        return None
   

def play_audio(filename):
    # play mp3 audio file
    import pygame
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

