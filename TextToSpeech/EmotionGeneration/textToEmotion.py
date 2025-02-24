import requests
import torch
from transformers import pipeline
import json
import numpy as np

emotion_mapping = {
    "joy": "joy",
    "anger": "anger",
    "fear": "fear",
    "sadness": "sadness",
    "disgust": "disgust",
    "surprise": "amazement",  
    "neutral": "cheekiness",  
    "anticipation": "outofbreath",
}

classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

def textToEmotion(text): 

    result = classifier(text)[0] 
    emotion_weights = {entry['label']: entry['score'] for entry in result}  
    
    mapped_emotions = {emotion_mapping.get(label, label): score for label, score in emotion_weights.items()}
    
    audio2face_emotions = {
        "amazement": mapped_emotions.get("amazement", 0),
        "anger": mapped_emotions.get("anger", 0),
        "cheekiness": mapped_emotions.get("cheekiness", 0),
        "disgust": mapped_emotions.get("disgust", 0),
        "fear": mapped_emotions.get("fear", 0),
        "grief": mapped_emotions.get("grief", 0),
        "joy": mapped_emotions.get("joy", 0),
        "outofbreath": mapped_emotions.get("outofbreath", 0),
        "pain": mapped_emotions.get("pain", 0),
        "sadness": mapped_emotions.get("sadness", 0)
    }
    
    return audio2face_emotions

def sendToAudio2Face(emotion_weights):
    url = 'http://localhost:8011/A2F/A2E/SetEmotionByName' 

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "a2f_instance": "/World/audio2face/CoreFullface",
        "emotions": emotion_weights
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Emotion weights sent to Audio2Face")
    else:
        print(f"Error sending emotion weights to Audio2Face: {response.status_code}, {response.text}")

def main():
    text = "Testing live gitignore"

    emotion_weights = textToEmotion(text)
    print(f"Emotion Weights: {emotion_weights}")
    sendToAudio2Face(emotion_weights)

if __name__ == "__main__":
    main()