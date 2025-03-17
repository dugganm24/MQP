import sys
import os
import time 
import asyncio
import subprocess 
import requests
import json
import torch 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Audio2Face", "EmotionGeneration")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Audio2Face", "SpeechGeneration")))

from textToEmotion import emotionGeneration, sendEmotionToAudio2Face
from textToSpeech import speechGeneration, sendSpeechToAudio2Face, playTrack

def start_ollama():
    ollama_path = r"C:\Users\mpduggan\AppData\Local\Programs\Ollama\ollama.exe"  

    try:
        process = subprocess.Popen([ollama_path, "run", "llama3.2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Ollama started successfully.")

        return process
    
    except Exception as e:
        print(f"Error starting Ollama: {e}")
        return None
    
async def generate_text(input_text):
    url = "http://localhost:11434/api/generate"  
    headers = {"Content-Type": "application/json"}  

    system_prompt = "You are a language model designed to generate text that will be converted into speech for a humanoid robot. Your responses should be clear and designed to be spoken aloud. Focus on providing informative and natural-sounding responses. While keeping the speech clear, provide enough details to fully answer the users question but keep responses as short as possible to minimize latency. Do not include any visual elements, like emojis, in your responses"

    data = {
        "model": "llama3.2",  
        "prompt": f"{system_prompt}\nUser input: {input_text}\nRobot speech:",
        "temperature": 0.1,
        "stop": ["<end_of_turn>"], 
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            response_json = response.json()
            return response_json.get("response", "No response key found.")
        else:
            return f"Error: {response.status_code}, {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

    
async def main():

    ollama_process = start_ollama()
    if ollama_process is None:
        print("Failed to start Ollama.")
        return

    
    input_text = input("Enter text: ")

    start_time = time.time()

    response_start_time = time.time() 
    response_text = await generate_text(input_text)
    response_end_time = time.time()
    print(f"Response: {response_text}")
    print(f"Response generation time: {response_end_time - response_start_time:.2f} seconds")


    speech_start_time = time.time()
    audioPath = await speechGeneration(response_text)
    speech_end_time = time.time()
    print(f"Speech generation time: {speech_end_time - speech_start_time:.2f} seconds")

    emotion_start_time = time.time()
    emotion_weights = await emotionGeneration(response_text)
    emotion_end_time = time.time()
    print(f"Emotion generation time: {emotion_end_time - emotion_start_time:.2f} seconds")

    send_emotion_start_time = time.time()
    await sendEmotionToAudio2Face(emotion_weights)
    send_emotion_end_time = time.time()
    print(f"Send emotion time: {send_emotion_end_time - send_emotion_start_time:.2f} seconds")

    send_speech_start_time = time.time()
    await sendSpeechToAudio2Face(audioPath)
    send_speech_end_time = time.time()
    print(f"Send speech time: {send_speech_end_time - send_speech_start_time:.2f} seconds")

    play_start_time = time.time()
    await playTrack()
    play_end_time = time.time()
    print(f"Play track time: {play_end_time - play_start_time:.2f} seconds")

    end_time = time.time()
    print(f"Total time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())