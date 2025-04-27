import librosa
import numpy as np
from audio import getAudio


def rate_singing(audio_path, frame_hop=5):
    getAudio(5)
    # Load the audio
    y, sr = librosa.load(audio_path)
    
    # Extract features
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

    # Get the mean energy
    energy = np.mean(librosa.feature.rms(y=y))
    
    # Focus only on the loudest pitch every few frames
    pitch_list = []
    for i in range(0, pitches.shape[1], frame_hop):  
        mag = magnitudes[:, i]
        pitch = pitches[:, i]
        if np.max(mag) > 0:
            index = np.argmax(mag)  
            pitch_value = pitch[index]
            if pitch_value > 0:
                pitch_list.append(pitch_value)
    
    pitch_array = np.array(pitch_list)
    pitch_variance = np.var(pitch_array) if len(pitch_array) > 0 else 1.0

    # Simple heuristics for scoring
    score = 10
    
    print(f"Tempo: {tempo}, Energy: {energy}, Pitch Variance: {pitch_variance}")

    if pitch_variance < 400000:
        score += 2  
        pitch_variance = 9
    elif pitch_variance < 430000:
        score += 0
        pitch_variance = 6
    elif pitch_variance < 450000:
        score -= 3  
        pitch_variance = 3
    else:
        score -= 7  
        pitch_variance = 1

    if energy > 0.15:
        score += 1
        energy = 10
    elif energy > 0.12:
        score += 0
        energy = 7
    else:
        score -= 4
        energy = 3

    if tempo < 40 or tempo > 200:
        score -= 3
        tempo = 3
    else:
        tempo = 8

    score = max(0, min(10, round(score)))
    print(f"🎤 Singing Rating for {audio_path}: {score}/10")

    return score, tempo, energy, pitch_variance

if __name__ == "__main__":
    audio_file = "output.wav"
    rating = rate_singing(audio_file)
    print(f"🎤 Singing Rating for {audio_file}: {rating}/10")
