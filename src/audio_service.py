import logging
import pyaudio
import wave

for _ in ("pyaudio", "wave"):
    logging.getLogger(_).setLevel(logging.CRITICAL)


def record_audio(duration=3, threshold=10, silence_threshold=200):
    """Record audio for a specified duration, 
    or until a pause in speech is detected."""

    # Set up audio input stream
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(
        format=FORMAT, 
        channels=CHANNELS, 
        rate=RATE, 
        input=True, 
        frames_per_buffer=CHUNK
    )

    frames = []
    silence_count = 0

    print("Listening...")

    # Record audio until duration or pause is detected
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

        # Check for pause in speech
        if max(data) < silence_threshold:
            silence_count += 1
        else:
            silence_count = 0

        # Stop recording if pause in speech is detected or duration is exceeded
        if silence_count > threshold or len(frames) >= duration * RATE / CHUNK:
            break

    print("Finished recording.")

    # Stop audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    return frames, RATE


def write_audio_to_file(frames, rate, filename):
    """Write recorded audio to a WAV file."""

    wf = wave.open(filename, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(rate)
    wf.writeframes(b"".join(frames))
    wf.close()


if __name__ == "__main__":
    frames, rate = record_audio()
    write_audio_to_file(frames, rate, "output.wav")
