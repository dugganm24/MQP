import requests
import torch
from transformers import pipeline
import json
import numpy as np
import aiohttp
import asyncio

device = 0 if torch.cuda.is_available() else -1

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

classifier = pipeline("text-classification", 
                      model="j-hartmann/emotion-english-distilroberta-base", 
                      top_k=None,
                      device = 0)

async def emotionGeneration(text): 

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

async def setIdleEmotion():
    idle_emotion = {
        "joy": 1.0,
        "anger": 0.0,
        "fear": 0.0,
        "sadness": 0.0,
        "disgust": 0.0,
        "amazement": 0.0,  
        "cheekiness": 0.0,  
        "outofbreath": 0.0
    }
    
    await sendEmotionToAudio2Face(idle_emotion)

async def sendEmotionToAudio2Face(emotion_weights):
    url = 'http://localhost:8011/A2F/A2E/SetEmotionByName' 

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "a2f_instance": "/World/audio2face/CoreFullface",
        "emotions": emotion_weights
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
            if response.status == 200:
                print("Emotion weights sent to Audio2Face")
            else:
                print(f"Error sending emotion weights to Audio2Face: {response.status}, {await response.text()}")