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

def textToEmotion(text):
    emotion_model = pipeline('text-classification', model='j-hartmann/emotion-english-distilroberta-base')

    result = emotion_model(text)
    emotion = result[0]['label'].lower()
    score = result[0]['score']

    return emotion, score

def generateEmotionWeights(emotion):
    emotion_weights = {
        "amazement": 0.0,
        "anger": 0.0,
        "cheekiness": 0.0,
        "disgust": 0.0,
        "fear": 0.0,
        "grief": 0.0,
        "joy": 0.0,
        "outofbreath": 0.0,
        "pain": 0.0,
        "sadness": 0.0
    }

    if emotion in emotion_mapping:
        audio2face_emotion = emotion_mapping[emotion]
        emotion_weights[audio2face_emotion] = 1.0 # initially set emotion to 1, can further customize this weight 
    
    return emotion_weights

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
        print("Emotions sent to Audio2Face")
    else:
        print(f"Error sending audio to Audio2Face: {response.status_code}, {response.text}")

def main():
    text = "Testing sadness, I am so sad"

    emotion, score = textToEmotion(text)
    print(f"Emotion: {emotion}, Score: {score}")

    emotion_weights = generateEmotionWeights(emotion)
    print(f"Emotion Weights: {emotion_weights}")

    sendToAudio2Face(emotion_weights)

if __name__ == "__main__":
    main()