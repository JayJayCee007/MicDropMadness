from audio_similarity import AudioSimilarity

# Paths to the original and compariosn audio files/folders
def fun():
    original_path = 'Real.mp3'
    generated_path = 'output.wav'

    # Set the sample rate and weights for the metrics

    sample_rate = 44100
    weights = {
        'zcr_similarity': 0.2,
        'rhythm_similarity': 0.2,
        'chroma_similarity': 0.2,
        'energy_envelope_similarity': 0.1,
        'spectral_contrast_similarity': 0.1,
        'perceptual_similarity': 0.2
    }

    # Instantiate the AudioSimilarity class
    audio_similarity = AudioSimilarity(original_path, generated_path, sample_rate, weights)

    # Calculate the stent weighted audio similarity
    similarity_score = audio_similarity.stent_weighted_audio_similarity()

    print(f"Stent Weighted Audio Similarity: {similarity_score}")
