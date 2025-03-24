import sys
import os
import time 
import asyncio
import subprocess 
import requests
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Audio2Face", "EmotionGeneration")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Audio2Face", "SpeechGeneration")))

from textToEmotion import emotionGeneration, sendEmotionToAudio2Face, setIdleEmotion
from textToSpeech import speechGeneration, sendSpeechToAudio2Face, playTrack, setIdleAudio, getResponseLength, setLooping

def start_ollama():
    ollama_path = r"C:\Users\mpduggan\AppData\Local\Programs\Ollama\ollama.exe"  

    try:
        process = subprocess.Popen([ollama_path, "run", "llama3.2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Ollama started successfully.")

        return process
    
    except Exception as e:
        print(f"Error starting Ollama: {e}")
        return None

async def idle_a2f():
    await setIdleAudio()
    await setIdleEmotion()
    await setLooping(True)
    await playTrack()    
    
async def generate_text(input_text):
    url = "http://localhost:11434/api/generate"  
    headers = {"Content-Type": "application/json"}  

    system_prompt = "You are a language model designed to generate text that will be converted into speech that will be said by a humanoid robot. Your responses should be clear and designed to be spoken aloud. Focus on providing informative and natural-sounding responses. While keeping the speech clear, provide enough details to fully answer the users question but keep responses as short as possible to minimize latency. Do not include any visual elements, like emojis, in your responses. Feel free to generate responses based on realistic emotions that a human would likely feel when applicable. Default to happy responses unless the prompt or user input suggests otherwise."

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
    
async def process_input(input_text):
    
    await setLooping(False)

    response_text = await generate_text(input_text)
    print(f"Response: {response_text}")

    audioPath = await speechGeneration(response_text)
    emotion_weights = await emotionGeneration(response_text)
    
    await sendEmotionToAudio2Face(emotion_weights)
    await sendSpeechToAudio2Face()

    await playTrack()

    response_length = await getResponseLength()
    start_of_response = response_length["result"]["default"][0]
    end_of_response = response_length["result"]["default"][1]
    track_duration = end_of_response - start_of_response
    await asyncio.sleep(track_duration)

    await idle_a2f()

async def main():

    ollama_process = start_ollama()
    if ollama_process is None:
        print("Failed to start Ollama.")
        return
    
    await idle_a2f()
            
    while True:
        input_text = input("Enter text: ")
        if input_text.lower() == "exit":
            break
            
        await process_input(input_text)

if __name__ == "__main__":
    asyncio.run(main())