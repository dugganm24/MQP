import pyttsx3
import requests
import os
import subprocess
import json
import aiohttp
import asyncio

async def speechGeneration(text):
    output_folder = "C:/Users/mpduggan/MQP/Audio2Face/SpeechGeneration/Output"

    file_path_wav = os.path.join(output_folder, "speechOutput.wav")
    file_path_wav = os.path.normpath(file_path_wav)

    def generate_speech(): 
        engine = pyttsx3.init()

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 150)

        engine.save_to_file(text, file_path_wav)
        engine.runAndWait()
    
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, generate_speech)

    return file_path_wav

async def sendSpeechToAudio2Face(audioPath):
    url = 'http://localhost:8011/A2F/Player/SetTrack'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "a2f_player": "/World/audio2face/Player",
        "file_name": audioPath, 
        "time_range": [0, -1]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
            if response.status == 200:
                print("Audio sent to Audio2Face")
            else:
                print(f"Error sending audio to Audio2Face: {response.status}, {await response.text()}")

async def playTrack():
    url = 'http://localhost:8011/A2F/Player/Play'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "a2f_player": "/World/audio2face/Player",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
            if response.status == 200:
                print("Audio played in Audio2Face")
            else:
                print(f"Error playing audio in Audio2Face: {response.status}, {await response.text()}")