from transformers import pipeline
import torch

classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

def get_emotion(text):
    model_outputs = classifier(text)
    emotion = model_outputs[0][0]['label']
    torch.cuda.empty_cache()
    return emotion