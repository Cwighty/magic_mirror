import asyncio
import websockets
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from audio_service import record_audio, write_audio_to_file
from llm_service import get_ai_response
from tts_service import get_text_to_speech, play_audio
from wake import listen_for_wake
from whisper_service import convert_to_text


async def notify_server(websocket, message):
    await websocket.send(message)

async def handle_detection():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await notify_server(websocket, "listening")
        print("Keyword detected!")
        frames, rate = record_audio()
        write_audio_to_file(frames, rate, "output.wav")
        
        await notify_server(websocket, "transcribing")
        print("Transcribing audio...")
        audio_file = open("output.wav", "rb")
        text = convert_to_text(audio_file)
        print("Transcription:", text)

        await notify_server(websocket, "processing")
        try:
            ai_res = get_ai_response(text)
            tts_audio_file = get_text_to_speech(ai_res)
        except Exception as e:
            tts_audio_file = "ChatServiceUnavailable.mp3"

        await notify_server(websocket, "processed " + tts_audio_file)


async def main():
    while True:
        await listen_for_wake(handle_detection)


if __name__ == "__main__":
    asyncio.run(main())