from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from audio_similarity import AudioSimilarity
from audioai import rate_singing
from Similarity import fun


def getText():
    audio_file = "output.wav"
    score, tempo, energy, pitch_variance = rate_singing(audio_file)

    tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")
    model = AutoModelForCausalLM.from_pretrained(
        "google/gemma-2b-it",
        torch_dtype=torch.bfloat16
    )

    songTitle = "From the Start by Laufey"
    input_text = (
        f"Give a rating out of 10 of the a karaoke performance based on the vibe of the song and the given stats. Give the number first than a two sentence very brief short explanation why the singer did a okay job of singing Song Title: {songTitle}. "
        f"Out of 10: Tempo: {tempo}, Out of 10: Energy: {energy}, Out of 10: Pitch Variance: {pitch_variance}, Out of 10: Other Score: {score} Start the response with the Rating also Laufey is Icelandic/Chinese "
    )

    input_ids = tokenizer(input_text, return_tensors="pt")

    outputs = model.generate(input_ids["input_ids"], max_length=200)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Remove the input prompt from the response
    ai_response = response[len(input_text):].strip()
    print(ai_response)
    # fun()
    return ai_response
