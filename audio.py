import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

# Settings
rate = 44100  # Hz
filename = "output.wav"
amplify_factor = 20.0  # How much louder you want (e.g., 2.0 = twice as loud)

def record_audio(duration, rate):
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * rate), samplerate=rate, channels=1, dtype='int16')
    sd.wait()
    return recording

def save_audio(data, rate, filename):
    wav.write(filename, rate, data)
    print(f"Audio saved to {filename}")

def amplify_audio(data, factor):
    # Amplify and clip to prevent overflow
    amplified = data.astype(np.float32) * factor
    amplified = np.clip(amplified, -32768, 32767)  # int16 limits
    return amplified.astype(np.int16)

def getAudio(duration):
    audio_data = record_audio(duration, rate)
    louder_audio = amplify_audio(audio_data, amplify_factor)
    save_audio(louder_audio, rate, filename)

